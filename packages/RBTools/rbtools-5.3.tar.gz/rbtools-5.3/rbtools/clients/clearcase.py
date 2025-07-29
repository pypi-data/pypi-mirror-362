"""A client for ClearCase."""

from __future__ import annotations

import io
import itertools
import logging
import os
import re
import sys
import threading
from collections import OrderedDict, defaultdict, deque
from typing import (Any, Dict, Iterable, List, Optional, TYPE_CHECKING, Tuple,
                    cast)

from pydiffx.dom import DiffX
from pydiffx.dom.objects import DiffXChangeSection
from typing_extensions import TypeAlias, TypedDict

from rbtools.api.errors import APIError
from rbtools.clients.base.repository import RepositoryInfo
from rbtools.clients.base.scmclient import (BaseSCMClient,
                                            SCMClientDiffResult,
                                            SCMClientRevisionSpec)
from rbtools.clients.errors import (InvalidRevisionSpecError,
                                    SCMClientDependencyError,
                                    SCMError)
from rbtools.diffs.writers import UnifiedDiffWriter
from rbtools.utils.checks import check_install
from rbtools.utils.filesystem import make_tempfile
from rbtools.utils.process import execute

# This specific import is necessary to handle the paths when running on cygwin.
if sys.platform.startswith(('cygwin', 'win')):
    import ntpath as cpath
else:
    import os.path as cpath

if TYPE_CHECKING:
    from rbtools.api.resource import ItemResource, ListResource

    _HostProperties: TypeAlias = Optional[Dict[str, str]]
    _ExtendedPath: TypeAlias = str
    _ChangedEntry: TypeAlias = Tuple[_ExtendedPath, _ExtendedPath]
    _ChangedEntryList: TypeAlias = Iterable[_ChangedEntry]

    #: Type for an entry with branched file versions.
    #:
    #: A 3-tuple containing the path, previous version, and current version.
    _BranchChangedEntry: TypeAlias = Tuple[str, str, str]


logger = logging.getLogger(__name__)


# This is used to split and assemble paths.
_MAIN = f'{os.sep}main{os.sep}'

_VERSION_CHECKEDOUT = sys.maxsize


class DirectoryDiff(TypedDict):
    """A difference between two directories.

    Version Added:
        5.0
    """

    #: The added files.
    #:
    #: Each entry is a tuple containing the new filename and new OID.
    added: set[tuple[str, str]]

    #: The deleted files.
    #:
    #: Each entry is a tuple containing the old filename and old OID.
    deleted: set[tuple[str, str]]

    #: The renamed files.
    #:
    #: Each entry is a tuple containing the old filename, old OID, new
    #: filename, and new OID.
    renamed: set[tuple[str, str, str, str]]


class LabelElementInfo(TypedDict):
    """Information about an element in a label.

    Version Added:
        5.0
    """

    #: The element's OID.
    oid: str

    #: The version of the element in the label.
    version: str


class _GetElementsFromLabelThread(threading.Thread):
    """A thread to collect results from ``cleartool find``.

    Collecting elements with ``cleartool find`` can take a long time. This
    thread allows us to do multiple finds concurrently.
    """

    def __init__(
        self,
        *,
        dir_name: str,
        label: str,
        elements: dict[str, LabelElementInfo],
        vob_tags: set[str],
    ) -> None:
        """Initialize the thread.

        Args:
            dir_name (str):
                The directory name to search.

            label (str):
                The label name.

            elements (dict):
                A dictionary mapping element path to an info dictionary. Each
                element contains ``oid`` and ``version`` keys.

            vob_tags (set of str):
                A list of the VOBs to search.
        """
        self.dir_name = dir_name
        self.elements = elements
        self.vob_tags = vob_tags

        # Remove any trailing VOB tag not supported by cleartool find.
        try:
            label, vobtag = label.rsplit('@', 1)
        except Exception:
            pass

        self.label = label

        super().__init__()

    def run(self) -> None:
        """Run the thread.

        This will store a dictionary of ClearCase elements (oid + version)
        belonging to a label and identified by path.
        """
        env = os.environ.copy()

        if sys.platform.startswith('win'):
            CLEARCASE_XPN = '%CLEARCASE_XPN%'
            CLEARCASE_PN = '%CLEARCASE_PN%'
            env['CLEARCASE_AVOBS'] = ';'.join(self.vob_tags)
        else:
            CLEARCASE_XPN = '$CLEARCASE_XPN'
            CLEARCASE_PN = '$CLEARCASE_PN'
            env['CLEARCASE_AVOBS'] = ':'.join(self.vob_tags)

        command = [
            'cleartool',
            'find',
            '-avobs',
        ]

        if self.label is None:
            command += [
                '-version',
                'lbtype(%s)' % self.label,
                '-exec',
                (f'cleartool describe -fmt "%On\t%En\t%Vn\n" '
                 f'"{CLEARCASE_XPN}"'),
            ]
        else:
            command = [
                '-exec',
                (f'cleartool describe -fmt "%On\t%En\t%Vn\n" '
                 f'"{CLEARCASE_PN}"'),
            ]

        output = execute(command,
                         extra_ignore_errors=(1,),
                         with_errors=False,
                         split_lines=True,
                         env=env)

        for line in output:
            # Skip any empty lines.
            if not line:
                continue

            oid, path, version = line.split('\t', 2)
            self.elements[path] = {
                'oid': oid,
                'version': version,
            }


class _ChangesetEntry:
    """An entry in a changeset.

    This is a helper class which wraps a changed element, and
    centralizes/caches various information about that element's old and new
    revisions.

    Version Added:
        3.0
    """

    def __init__(
        self,
        *,
        root_path: str,
        old_path: Optional[str] = None,
        new_path: Optional[str] = None,
        old_oid: Optional[str] = None,
        new_oid: Optional[str] = None,
        op: str = 'modify',
        is_dir: bool = False,
    ) -> None:
        """Initialize the changeset entry.

        Args:
            root_path (str):
                The root path of the view.

            old_path (str, optional):
                The extended path of the "old" version of the element.

            new_path (str, optional):
                The extended path of the "new" version of the element.

            old_oid (str, optional):
                The OID of the "old" version of the element.

            new_oid (str, optional):
                The OID of the "new" version of the element.

            op (str, optional):
                The change operation.

            is_dir (bool, optional):
                Whether the changeset entry represents a directory.
        """
        self.root_path = root_path

        self.old_path = old_path
        self._old_name = None
        self._old_oid = old_oid
        self._old_version = None

        self.new_path = new_path
        self._new_name = None
        self._new_oid = new_oid
        self._new_version = None

        self._vob_oid = None

        self.op = op
        self.is_dir = is_dir

    @property
    def vob_oid(self) -> str:
        """The OID of the VOB that the element is in.

        Type:
            str
        """
        if self._vob_oid is None:
            self._vob_oid = execute(
                ['cleartool', 'describe', '-fmt', '%On',
                 'vob:%s' % (self.new_path or self.old_path)])

        return self._vob_oid

    @property
    def old_oid(self) -> str:
        """The OID of the old version of the element.

        Type:
            str
        """
        if self._old_oid is None:
            if self.old_path:
                self._old_oid = execute(['cleartool', 'describe', '-fmt',
                                         '%On', self.old_path])
            else:
                self._old_oid = '0'

        return self._old_oid

    @property
    def old_name(self) -> Optional[str]:
        """The name of the old version of the element.

        Type:
            str:
        """
        if self._old_name is None and self.old_path:
            self._old_name = os.path.relpath(
                execute(['cleartool', 'describe', '-fmt', '%En',
                         self.old_path]),
                self.root_path)

        return self._old_name

    @property
    def old_version(self) -> Optional[str]:
        """The version of the old version of the element.

        Type:
            str
        """
        if self._old_version is None and self.old_path:
            self._old_version = execute(
                ['cleartool', 'describe', '-fmt', '%Vn',
                 f'oid:{self.old_oid}@vobuuid:{self.vob_oid}'])

        return self._old_version

    @property
    def new_oid(self) -> str:
        """The OID of the new version of the element.

        Type:
            str
        """
        if self._new_oid is None:
            if self.new_path:
                self._new_oid = execute(['cleartool', 'describe', '-fmt',
                                         '%On', self.new_path])
            else:
                self._new_oid = '0'

        return self._new_oid

    @property
    def new_name(self) -> Optional[str]:
        """The name of the new version of the element.

        Type:
            str:
        """
        if self._new_name is None and self.new_path:
            self._new_name = os.path.relpath(
                execute(['cleartool', 'describe', '-fmt', '%En',
                         self.new_path]),
                self.root_path)

        return self._new_name

    @property
    def new_version(self) -> Optional[str]:
        """The version of the new version of the element.

        Type:
            str
        """
        if self._new_version is None and self.new_path:
            self._new_version = execute(
                ['cleartool', 'describe', '-fmt', '%Vn',
                 f'oid:{self.new_oid}@vobuuid:{self.vob_oid}'],
                ignore_errors=True,
                with_errors=True)

            if 'Not a vob object' in self._new_version:
                self._new_version = 'CHECKEDOUT'

        return self._new_version

    def __repr__(self) -> str:
        """Return a representation of the object.

        Returns:
            str:
            The internal representation of the object.
        """
        return (
            f'<_ChangesetEntry op={self.op} old_path={self.old_path} '
            f'new_path={self.new_path}>')


class ClearCaseClient(BaseSCMClient):
    """A client for ClearCase.

    This is a wrapper around the clearcase tool that fetches repository
    information and generates compatible diffs. This client assumes that cygwin
    is installed on Windows.
    """

    scmclient_id = 'clearcase'
    name = 'ClearCase'

    # Review Board versions that use the old names-based repositories/?tool=
    # API parameter also have a bug where a missing name could cause a
    # server-side crash. This was making it so servers that did not have Power
    # Pack were failing when we tried to make a query that included the
    # VersionVault name. We therefore only include it when we know the server
    # can use server_tool_ids instead.
    server_tool_names = 'ClearCase,VersionVault / ClearCase'
    server_tool_ids = ['clearcase', 'versionvault']

    requires_diff_tool = True

    supports_patch_revert = True

    REVISION_ACTIVITY_BASE = '--rbtools-activity-base'
    REVISION_ACTIVITY_PREFIX = 'activity:'
    REVISION_BASELINE_BASE = '--rbtools-baseline-base'
    REVISION_BASELINE_PREFIX = 'baseline:'
    REVISION_BRANCH_BASE = '--rbtools-branch-base'
    REVISION_BRANCH_PREFIX = 'brtype:'
    REVISION_CHECKEDOUT_BASE = '--rbtools-checkedout-base'
    REVISION_CHECKEDOUT_CHANGESET = '--rbtools-checkedout-changeset'
    REVISION_FILES = '--rbtools-files'
    REVISION_LABEL_BASE = '--rbtools-label-base'
    REVISION_LABEL_PREFIX = 'lbtype:'
    REVISION_STREAM_BASE = '--rbtools-stream-base'
    REVISION_STREAM_PREFIX = 'stream:'

    CHECKEDOUT_RE = re.compile(r'CHECKEDOUT(\.\d+)?$')

    ######################
    # Instance variables #
    ######################

    #: Whether the ClearCase setup is using UCM.
    is_ucm: bool

    #: The name of the user's view.
    viewname: Optional[str]

    #: The user's ClearCase view type.
    #:
    #: This will be either ``snapshot`` or ``dynamic``.
    viewtype: Optional[str]

    #: The current repository's VOB tag.
    #:
    #: This is only used for matching the Review Board server repository.
    vobtag: Optional[str]

    def __init__(
        self,
        **kwargs,
    ) -> None:
        """Initialize the client.

        Args:
            **kwargs (dict):
                Keyword arguments to pass through to the superclass.
        """
        super().__init__(**kwargs)
        self.viewtype = None
        self.viewname = None
        self.is_ucm = False
        self.vobtag = None

        self._host_properties: _HostProperties = None
        self._host_properties_set: bool = False

    @property
    def host_properties(self) -> _HostProperties:
        """A dictionary containing host properties.

        This will fetch the properties on first access, and cache for future
        usage.

        The contents are the results of :command:`cleartool hostinfo -l`, with
        the addition of:

        Keys:
            Product name (str):
                The name portion of the ``Product`` key.

            Product version (str):
                The version portion of the ``Product`` key.

        Callers must call :py:meth:`setup` or :py:meth:`has_dependencies`
        before accessing this.

        They also must check for ``None`` responses and exceptions.

        Version Changed:
            4.0:
            Made this a lazily-loaded caching property.

        Type:
            dict

        Raises:
            rbtools.clients.errors.SCMError:
                There was an error fetching host property information.
        """
        if not self._host_properties_set:
            self._host_properties = self._get_host_info()
            self._host_properties_set = True

        return self._host_properties

    def check_dependencies(self) -> None:
        """Check whether all dependencies for the client are available.

        This will check for :command:`cleartool` in the path.

        Version Added:
            4.0

        Raises:
            rbtools.clients.errors.SCMClientDependencyError:
                :command:`cleartool` could not be found.
        """
        if not check_install(['cleartool', 'help']):
            raise SCMClientDependencyError(missing_exes=['cleartool'])

    def get_local_path(self) -> Optional[str]:
        """Return the local path to the working tree.

        Returns:
            str:
            The filesystem path of the repository on the client system.
        """
        # NOTE: This can be removed once check_dependencies() is mandatory.
        if not self.has_dependencies(expect_checked=True):
            logger.debug('Unable to execute "cleartool help": skipping '
                         'ClearCase')
            return None

        # Bail out early if we're not in a view.
        self.viewname = execute(['cleartool', 'pwv', '-short']).strip()

        if self.viewname.startswith('** NONE'):
            return None

        # Get the root path of the view.
        self.root_path = execute(['cleartool', 'pwv', '-root'],
                                 ignore_errors=True).strip()

        if 'Error: ' in self.root_path:
            raise SCMError('Failed to generate diff run rbt inside view.')

        vobtag = self._get_vobtag()

        return os.path.join(self.root_path, vobtag)

    def get_repository_info(self) -> Optional[RepositoryInfo]:
        """Return repository information for the current working tree.

        Returns:
            ClearCaseRepositoryInfo:
            The repository info structure.
        """
        local_path = self.get_local_path()

        if not local_path:
            return None

        property_lines = execute(
            ['cleartool', 'lsview', '-full', '-properties', '-cview'],
            split_lines=True)

        for line in property_lines:
            properties = line.split(' ')

            if properties[0] == 'Properties:':
                # Determine the view type and check if it's supported.
                if 'automatic' in properties or 'webview' in properties:
                    # These are checked first because automatic views and
                    # webviews with both also list "snapshot", but won't be
                    # usable as a snapshot view.
                    raise SCMError('Webviews and automatic views are not '
                                   'currently supported. RBTools commands can '
                                   'only be used in dynamic or snapshot '
                                   'views.')
                elif 'snapshot' in properties:
                    self.viewtype = 'snapshot'
                elif 'dynamic' in properties:
                    self.viewtype = 'dynamic'
                else:
                    raise SCMError('Unable to determine the view type. '
                                   'RBTools commands can only be used in '
                                   'dynamic or snapshot views.')

                self.is_ucm = 'ucmview' in properties

                break

        return ClearCaseRepositoryInfo(path=local_path,
                                       vobtag=self._get_vobtag())

    def find_matching_server_repository(
        self,
        repositories: ListResource,
    ) -> tuple[Optional[ItemResource], Optional[ItemResource]]:
        """Find a match for the repository on the server.

        Args:
            repositories (rbtools.api.resource.ListResource):
                The fetched repositories.

        Returns:
            tuple:
            A 2-tuple of :py:class:`~rbtools.api.resource.ItemResource`. The
            first item is the matching repository, and the second is the
            repository info resource.
        """
        vobtag = self._get_vobtag()
        uuid = self._get_vob_uuid(vobtag)

        # To reduce calls to fetch the repository info resource (which can be
        # expensive to compute on the server and isn't cacheable), we build an
        # ordered list of ClearCase repositories starting with the ones that
        # have a similar vobtag.
        repository_scan_order = deque()

        # Because the VOB tag is platform-specific, we split and search for the
        # remote name in any sub-part so the request optimiziation can work for
        # users on both Windows and Unix-like platforms.
        vobtag_parts = vobtag.split(cpath.sep)

        for repository in repositories.all_items:
            repo_name = repository['name']

            # Repositories with a name similar to the VOB tag get put at the
            # beginning, and others at the end.
            if repo_name == vobtag or repo_name in vobtag_parts:
                repository_scan_order.appendleft(repository)
            else:
                repository_scan_order.append(repository)

        # Now scan through and look for a repository with a matching UUID.
        for repository in repository_scan_order:
            try:
                info = repository.get_info()
            except APIError:
                continue

            if not info:
                continue

            # There are two possibilities here. The ClearCase SCMTool shipped
            # with Review Board is now considered a legacy implementation, and
            # supports a single VOB (the "uuid" case). The new VersionVault
            # tool (which supports IBM ClearCase as well) ships with Power
            # Pack, and supports multiple VOBs (the "uuids" case).
            if (('uuid' in info and uuid == info['uuid']) or
                ('uuids' in info and uuid in info['uuids'])):
                return repository, info

        return None, None

    def parse_revision_spec(
        self,
        revisions: list[str] = [],
    ) -> SCMClientRevisionSpec:
        """Parse the given revision spec.

        These will be used to generate the diffs to upload to Review Board
        (or print).

        There are many different ways to generate diffs for ClearCase,
        because there are so many different workflows. This method serves
        more as a way to validate the passed-in arguments than actually
        parsing them in the way that other clients do.

        Args:
            revisions (list of str, optional):
                A list of revisions as specified by the user.

        Returns:
            dict:
            The parsed revision spec.

            See :py:class:`~rbtools.clients.base.scmclient.
            SCMClientRevisionSpec` for the format of this dictionary.

            This always populates ``base`` and ``tip``.

        Raises:
            rbtools.clients.errors.InvalidRevisionSpecError:
                The given revisions could not be parsed.

            rbtools.clients.errors.TooManyRevisionsError:
                The specified revisions list contained too many revisions.
        """
        n_revs = len(revisions)

        if n_revs == 0:
            return {
                'base': self.REVISION_CHECKEDOUT_BASE,
                'tip': self.REVISION_CHECKEDOUT_CHANGESET,
            }
        elif n_revs == 1:
            revision = revisions[0]

            if revision.startswith(self.REVISION_ACTIVITY_PREFIX):
                return {
                    'base': self.REVISION_ACTIVITY_BASE,
                    'tip': revision[len(self.REVISION_ACTIVITY_PREFIX):],
                }
            elif revision.startswith(self.REVISION_BASELINE_PREFIX):
                tip = revision[len(self.REVISION_BASELINE_PREFIX):]

                if len(tip.rsplit('@', 1)) != 2:
                    raise InvalidRevisionSpecError(
                        'Baseline name %s must include a PVOB tag' % tip)

                return {
                    'base': self.REVISION_BASELINE_BASE,
                    'tip': [tip],
                }
            elif revision.startswith(self.REVISION_BRANCH_PREFIX):
                return {
                    'base': self.REVISION_BRANCH_BASE,
                    'tip': revision[len(self.REVISION_BRANCH_PREFIX):],
                }
            elif revision.startswith(self.REVISION_LABEL_PREFIX):
                return {
                    'base': self.REVISION_LABEL_BASE,
                    'tip': [revision[len(self.REVISION_BRANCH_PREFIX):]],
                }
            elif revision.startswith(self.REVISION_STREAM_PREFIX):
                tip = revision[len(self.REVISION_STREAM_PREFIX):]

                if len(tip.rsplit('@', 1)) != 2:
                    raise InvalidRevisionSpecError(
                        f'UCM stream name {tip} must include a PVOB tag')

                return {
                    'base': self.REVISION_STREAM_BASE,
                    'tip': tip,
                }
        elif n_revs == 2:
            if self.viewtype != 'dynamic':
                raise SCMError('To generate a diff using multiple revisions, '
                               'you must use a dynamic view.')

            if (revisions[0].startswith(self.REVISION_BASELINE_PREFIX) and
                revisions[1].startswith(self.REVISION_BASELINE_PREFIX)):
                tips = [
                    revision[len(self.REVISION_BASELINE_PREFIX):]
                    for revision in revisions
                ]

                pvobs = []

                for tip in tips:
                    try:
                        pvobs.append(tip.rsplit('@', 1)[1])
                    except KeyError:
                        raise InvalidRevisionSpecError(
                            'Baseline name %s must include a PVOB tag' % tip)

                if pvobs[0] != pvobs[1]:
                    raise InvalidRevisionSpecError(
                        f'Baselines {pvobs[0]} and {pvobs[1]} do not have '
                        f'the same PVOB tag')

                return {
                    'base': self.REVISION_BASELINE_BASE,
                    'tip': tips,
                }
            elif (revisions[0].startswith(self.REVISION_LABEL_PREFIX) and
                  revisions[1].startswith(self.REVISION_LABEL_PREFIX)):
                return {
                    'base': self.REVISION_LABEL_BASE,
                    'tip': [
                        revision[len(self.REVISION_BRANCH_PREFIX):]
                        for revision in revisions
                    ],
                }

        # None of the "special" types have been found. Assume that the list of
        # items are one or more pairs of files to compare.
        pairs = []

        for r in revisions:
            p = r.split(':')

            if len(p) != 2:
                raise InvalidRevisionSpecError(
                    '"%s" is not a valid file@revision pair' % r)

            pairs.append(p)

        return {
            'base': self.REVISION_FILES,
            'tip': pairs,
        }

    def diff(
        self,
        revisions: SCMClientRevisionSpec,
        *,
        include_files: list[str] = [],
        exclude_patterns: list[str] = [],
        repository_info: ClearCaseRepositoryInfo,
        extra_args: list[str] = [],
        **kwargs,
    ) -> SCMClientDiffResult:
        """Perform a diff using the given revisions.

        Args:
            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            include_files (list of str, optional):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of str, optional):
                A list of shell-style glob patterns to blacklist during diff
                generation.

            repository_info (ClearCaseRepositoryInfo, optional):
                The repository info structure.

            extra_args (list, unused):
                Additional arguments to be passed to the diff generation.
                Unused for ClearCase.

            **kwargs (dict, optional):
                Unused keyword arguments.

        Returns:
            dict:
            A dictionary containing the following keys:

            ``diff`` (:py:class:`bytes`):
                The contents of the diff to upload.
        """
        if include_files:
            raise SCMError(
                'The ClearCase backend does not currently support the '
                '-I/--include parameter. To diff for specific files, pass in '
                'file@revision1:file@revision2 pairs as arguments')

        base = revisions['base']
        tip = revisions['tip']

        if tip == self.REVISION_CHECKEDOUT_CHANGESET:
            changelist = self._get_checkedout_changelist(repository_info)
        elif base == self.REVISION_ACTIVITY_BASE:
            assert isinstance(tip, str)

            changelist = self._get_activity_changelist(tip, repository_info)
        elif base == self.REVISION_BASELINE_BASE:
            assert isinstance(tip, list)

            changelist = self._get_baseline_changelist(tip)
        elif base == self.REVISION_BRANCH_BASE:
            assert isinstance(tip, str)

            changelist = self._get_branch_changelist(tip, repository_info)
        elif base == self.REVISION_LABEL_BASE:
            assert isinstance(tip, list)

            changelist = self._get_label_changelist(tip, repository_info)
        elif base == self.REVISION_STREAM_BASE:
            assert isinstance(tip, str)

            changelist = self._get_stream_changelist(tip, repository_info)
        elif base == self.REVISION_FILES:
            assert isinstance(tip, list)

            changelist = tip
        else:
            assert False

        metadata = self._get_diff_metadata(revisions)

        return self._do_diff(changelist, repository_info, metadata)

    def _get_vobtag(self) -> str:
        """Return the current repository's VOB tag.

        Returns:
            str:
            The VOB tag for the current working directory.

        Raises:
            rbtools.clients.errors.SCMError:
                The VOB tag was unable to be determined.
        """
        if not self.vobtag:
            self.vobtag = execute(['cleartool', 'describe', '-short', 'vob:.'],
                                  ignore_errors=True).strip()

            if 'Error: ' in self.vobtag:
                raise SCMError('Unable to determine the current VOB. Make '
                               'sure to run RBTools from within your '
                               'ClearCase view.')

        return self.vobtag

    def _get_vob_uuid(
        self,
        vobtag: str,
    ) -> Optional[str]:
        """Return the current VOB's UUID.

        Args:
            vobtag (str):
                The VOB tag to query.

        Returns:
            str:
            The VOB UUID.
        """
        property_lines = execute(
            ['cleartool', 'lsvob', '-long', vobtag],
            split_lines=True)

        for line in property_lines:
            if line.startswith('Vob family uuid:'):
                return line.split(' ')[-1].rstrip()

        return None

    def _is_a_label(
        self,
        label: str,
        vobtag: str,
    ) -> bool:
        """Return whether a given label is a valid ClearCase lbtype.

        Args:
            label (str):
                The label to check.

            vobtag (str):
                The VOB tag to limit the label to.

        Raises:
            rbtools.clients.errors.SCMError:
                The VOB tag did not match.

        Returns:
            bool:
            Whether the label was valid.
        """
        label_vobtag = None

        # Try to find any vobtag.
        try:
            label, label_vobtag = label.rsplit('@', 1)
        except Exception:
            pass

        # Be sure label is prefix by lbtype, required by cleartool describe.
        if not label.startswith(self.REVISION_LABEL_PREFIX):
            label = f'{self.REVISION_LABEL_PREFIX}{label}'

        # If vobtag defined, check if it matches with the one extracted from
        # label, otherwise raise an exception.
        if vobtag and label_vobtag and label_vobtag != vobtag:
            raise SCMError(
                f'label vobtag {label_vobtag} does not match expected vobtag '
                f'{vobtag}')

        # Finally check if label exists in database, otherwise quit. Ignore
        # return code 1, it means label does not exist.
        output = execute(['cleartool', 'describe', '-short', label],
                         extra_ignore_errors=(1,),
                         with_errors=False)
        return bool(output)

    def _determine_version(
        self,
        version_path: str,
    ) -> int:
        """Determine the numeric version of a version path.

        This will split a version path, pulling out the branch and version. A
        special version value of ``CHECKEDOUT`` represents the latest version
        of a file, similar to ``HEAD`` in many other types of repositories.

        Args:
            version_path (str):
                A version path consisting of a branch path and a version
                number.

        Returns:
            int:
            The numeric portion of the version path.
        """
        branch, number = cpath.split(version_path)

        if self.CHECKEDOUT_RE.search(number):
            return _VERSION_CHECKEDOUT

        return int(number)

    def _construct_extended_path(
        self,
        path: str,
        version: str,
    ) -> str:
        """Construct an extended path from a file path and version identifier.

        This will construct a path in the form of ``path@version``. If the
        version is the special value ``CHECKEDOUT``, only the path will be
        returned.

        Args:
            path (str):
                A file path.

            version (str):
                The version of the file.

        Returns:
            str:
            The combined extended path.
        """
        if not version or self.CHECKEDOUT_RE.search(version):
            return path

        return f'{path}@@{version}'

    def _construct_revision(
        self,
        branch_path: str,
        version_number: str,
    ) -> str:
        """Construct a revisioned path from a branch path and version ID.

        Args:
            branch_path (str):
                The path of a branch.

            version_number (str):
                The version number of the revision.

        Returns:
            str:
            The combined revision.
        """
        return cpath.join(branch_path, version_number)

    def _get_previous_version(
        self,
        path: str,
        branch_path: str,
        version_number: str,
    ) -> tuple[str, str]:
        """Return the previous version for a ClearCase versioned element.

        The previous version of an element can usually be found by simply
        decrementing the version number at the end of an extended path, but it
        is possible to use `cleartool rmver` to remove individual versions.
        This method will query ClearCase for the predecessor version.

        Args:
            path (str):
                The path to an element.

            branch_path (str):
                The path of the branch of the element (typically something like
                /main/).

            version_number (int):
                The version number of the element.

        Returns:
            tuple:
            A 2-tuple consisting of the predecessor branch path and version
            number.
        """
        full_version = cpath.join(branch_path, str(version_number))
        extended_path = f'{path}@@{full_version}'

        previous_version = execute(
            ['cleartool', 'desc', '-fmt', '%[version_predecessor]p',
             extended_path],
            ignore_errors=True).strip()

        if 'Error' in previous_version:
            raise SCMError('Unable to find the predecessor version for %s'
                           % extended_path)

        return cpath.split(previous_version)

    def _sanitize_branch_changeset(
        self,
        changed_items: list[_BranchChangedEntry],
    ) -> _ChangedEntryList:
        """Return changeset containing non-binary, branched file versions.

        Changeset contain only first and last version of file made on branch.

        Args:
            changed_items (list of _BranchChangedEntry):
                The list of changed items.

        Yields:
            _ChangedEntry:
            Each entry in the branch.
        """
        changes_by_path: dict[str, dict[str, Any]] = {}

        for path, previous, current in changed_items:
            version_number = self._determine_version(current)

            if path not in changes_by_path:
                changes_by_path[path] = {
                    'highest': version_number,
                    'current': current,
                    'previous': previous,
                }
            elif version_number == 0:
                # Previous version of 0 version on branch is base
                changes_by_path[path]['previous'] = previous
            elif version_number > changes_by_path[path]['highest']:
                changes_by_path[path]['highest'] = version_number
                changes_by_path[path]['current'] = current

        for path, version in changes_by_path.items():
            yield (
                self._construct_extended_path(path, version['previous']),
                self._construct_extended_path(path, version['current']),
            )

    def _sanitize_version_0_file(
        self,
        file_revision: str,
    ) -> str:
        """Sanitize a version 0 file.

        This fixes up a revision identifier to use the correct predecessor
        revision when the version is 0. ``/main/0`` is a special case which is
        left as-is.

        Args:
            file_revision (str):
                The file revision to sanitize.

        Returns:
            str:
            The sanitized revision.
        """
        # There is no predecessor for @@/main/0, so keep current revision.
        if file_revision.endswith('%s0' % _MAIN):
            return file_revision

        if file_revision.endswith('%s0' % os.sep):
            logger.debug('Found file %s with version 0', file_revision)
            file_revision = execute(['cleartool',
                                     'describe',
                                     '-fmt', '%En@@%PSn',
                                     file_revision])
            logger.debug('Sanitized with predecessor, new file: %s',
                         file_revision)

        return file_revision

    def _sanitize_version_0_changeset(
        self,
        changeset: _ChangedEntryList,
    ) -> _ChangedEntryList:
        """Return changeset sanitized of its <branch>/0 version.

        Indeed this predecessor (equal to <branch>/0) should already be
        available from previous vob synchro in multi-site context.

        Args:
            changeset (list):
                A list of changes in the changeset.

        Yields:
            _ChangedEntry:
            Each changed entry in the changeset.
        """
        for old_file, new_file in changeset:
            # This should not happen for new file but it is safer to sanitize
            # both file revisions.
            yield (
                self._sanitize_version_0_file(old_file),
                self._sanitize_version_0_file(new_file),
            )

    def _get_checkedout_changelist(
        self,
        repository_info: ClearCaseRepositoryInfo,
    ) -> _ChangedEntryList:
        """Return information about the checked out changeset.

        This function returns: kind of element, path to file, previous and
        current file version.

        Args:
            repository_info (ClearCaseRepositoryInfo):
                The repository info structure.

        Yields:
            _ChangedEntry:
            Each changed entry in the checkout.
        """
        env = os.environ.copy()

        if sys.platform.startswith('win'):
            env['CLEARCASE_AVOBS'] = ';'.join(repository_info.vob_tags)
        else:
            env['CLEARCASE_AVOBS'] = ':'.join(repository_info.vob_tags)

        # We ignore return code 1 in order to omit files that ClearCase can't
        # read.
        output = execute(
            [
                'cleartool',
                'lscheckout',
                '-avobs',
                '-cview',
                '-me',
                '-fmt',
                r'%En\t%PVn\t%Vn\n',
            ],
            extra_ignore_errors=(1,),
            with_errors=False,
            env=env,
            split_lines=True)

        for line in output:
            path, previous, current = line.strip().split('\t')

            yield (
                self._construct_extended_path(path, previous),
                self._construct_extended_path(path, current),
            )

    def _get_activity_changelist(
        self,
        activity: str,
        repository_info: ClearCaseRepositoryInfo,
    ) -> _ChangedEntryList:
        """Return information about the versions changed on a branch.

        This takes into account the changes attached to this activity
        (including rebase changes) in all vobs of the current view.

        Args:
            activity (str):
                The activity name.

            repository_info (ClearCaseRepositoryInfo):
                The repository info structure.

        Yields:
            _ChangedEntry:
            Each changed entry in the activity.
        """
        changed_items: list[str] = []

        # Get list of revisions and get the diff of each one. Return code 1 is
        # ignored in order to omit files that ClearCase can't read.
        output = execute(['cleartool',
                          'lsactivity',
                          '-fmt',
                          '%[versions]Qp',
                          activity],
                         extra_ignore_errors=(1,),
                         with_errors=False)

        if output:
            # UCM activity changeset with %[versions]Qp is split by spaces but
            # not EOL. However, since each version is enclosed in double
            # quotes, we can split and consolidate the list.
            changed_items = cast(List[str], filter(
                None,
                (x.strip() for x in output.split('"'))))

        # Accumulate all changes to find the lowest and highest versions.
        changes_by_path: OrderedDict[str, dict[str, Any]] = OrderedDict()
        ignored_changes: list[str] = []

        for item in changed_items:
            path, current = item.rsplit(_MAIN, 1)

            if path.endswith('@@'):
                path = path[:-2]

            current = _MAIN + current

            # If a file isn't in the correct vob, ignore it.
            for tag in repository_info.vob_tags:
                if f'{tag}{os.sep}' in path:
                    break
            else:
                logger.debug('VOB tag does not match, ignoring changes on %s',
                             path)
                ignored_changes.append(item)
                continue

            version = self._determine_version(current)

            if path not in changes_by_path:
                changes_by_path[path] = {
                    'highest': version,
                    'lowest': version,
                    'current': current,
                }
            elif version > changes_by_path[path]['highest']:
                changes_by_path[path]['highest'] = version
                changes_by_path[path]['current'] = current
            elif version < changes_by_path[path]['lowest']:
                changes_by_path[path]['lowest'] = version

        if ignored_changes:
            logger.warning(
                'The following elements from this change set are not part '
                'of the currently configured repository, and will be '
                'ignored:')

            for change in ignored_changes:
                logger.warning(change)

        for path, version_info in changes_by_path.items():
            current = version_info['current']
            branch_path, current_version = cpath.split(current)

            lowest = version_info['lowest']

            if lowest == _VERSION_CHECKEDOUT:
                # This is a new file in the workspace.
                prev_version = '0'
            else:
                # Query for the previous version, just in case an old revision
                # was removed.
                branch_path, prev_version = self._get_previous_version(
                    path, branch_path, lowest)

            previous = self._construct_revision(branch_path, prev_version)

            yield (
                self._construct_extended_path(path, previous),
                self._construct_extended_path(path, current),
            )

    def _get_baseline_changelist(
        self,
        baselines: list[str],
    ) -> _ChangedEntryList:
        """Return information about versions changed between two baselines.

        Args:
            baselines (list of str):
                A list of one or two baselines including PVOB tags. If one
                baseline is included, this will do a diff between that and the
                predecessor baseline.

        Returns:
            list:
            A list of the changed files.
        """
        command = [
            'cleartool',
            'diffbl',
            '-version',
        ]

        if len(baselines) == 1:
            command += [
                '-predecessor',
                f'baseline:{baselines[0]}',
            ]
        else:
            command += [
                f'baseline:{baselines[0]}',
                f'baseline:{baselines[1]}',
            ]

        diff = execute(command,
                       extra_ignore_errors=(1, 2),
                       split_lines=True)

        WS_RE = re.compile(r'\s+')
        versions = [
            WS_RE.split(line.strip(), 1)[1]
            for line in diff
            if line.startswith(('>>', '<<'))
        ]

        version_info = filter(None, [
            execute(
                [
                    'cleartool',
                    'describe',
                    '-fmt',
                    '%En\t%PVn\t%Vn\n',
                    version,
                ],
                extra_ignore_errors=(1,),
                results_unicode=True)
            for version in versions
        ])

        entry_lines = ''.join(version_info).split('\n')

        changed_items = cast(List[_BranchChangedEntry], [
            line.strip().split('\t')
            for line in entry_lines
        ])

        return self._sanitize_branch_changeset(changed_items)

    def _get_branch_changelist(
        self,
        branch: str,
        repository_info: ClearCaseRepositoryInfo,
    ) -> _ChangedEntryList:
        """Return information about the versions changed on a branch.

        This takes into account the changes on the branch owned by the
        current user in all vobs of the current view.

        Args:
            branch (str):
                The branch name.

            repository_info (ClearCaseRepositoryInfo):
                The repository info structure.

        Returns:
            list:
            A list of the changed files.
        """
        env = os.environ.copy()

        if sys.platform.startswith('win'):
            CLEARCASE_XPN = '%CLEARCASE_XPN%'
            env['CLEARCASE_AVOBS'] = ';'.join(repository_info.vob_tags)
        else:
            CLEARCASE_XPN = '$CLEARCASE_XPN'
            env['CLEARCASE_AVOBS'] = ':'.join(repository_info.vob_tags)

        # We ignore return code 1 in order to omit files that ClearCase can't
        # read.
        output = execute(
            [
                'cleartool',
                'find',
                '-avobs',
                '-version',
                'brtype(%s)' % branch,
                '-exec',
                (f'cleartool descr -fmt "%En\t%PVn\t%Vn\n" '
                 f'"{CLEARCASE_XPN}"'),
            ],
            extra_ignore_errors=(1,),
            with_errors=False,
            env=env,
            split_lines=True)

        changed_items = cast(List[_BranchChangedEntry], [
            line.strip().split('\t')
            for line in output
        ])

        return self._sanitize_branch_changeset(changed_items)

    def _get_label_changelist(
        self,
        labels: list[str],
        repository_info: ClearCaseRepositoryInfo,
    ) -> _ChangedEntryList:
        """Return information about the versions changed between labels.

        This takes into account the changes done between labels and restrict
        analysis to current working directory. A ClearCase label belongs to a
        unique vob.

        Args:
            labels (list):
                A list of labels to compare.

            repository_info (ClearCaseRepositoryInfo):
                The repository info structure.

        Yields:
            _ChangedEntry:
            Each entry changed between the two labels.
        """
        # Initialize comparison_path to current working directory.
        # TODO: support another argument to manage a different comparison path.
        comparison_path = os.getcwd()

        error_message = None

        try:
            if len(labels) == 1:
                labels.append('LATEST')

            assert len(labels) == 2

            matched_vobs = set()

            for tag in repository_info.vob_tags:
                labels_present = True

                for label in labels:
                    if label != 'LATEST' and not self._is_a_label(label, tag):
                        labels_present = False

                if labels_present:
                    matched_vobs.add(tag)

            if not matched_vobs:
                raise SCMError(
                    'Labels %r were not found in any of the configured VOBs'
                    % labels)

            previous_label, current_label = labels
            logger.debug('Comparison between labels %s and %s on %s',
                         previous_label, current_label, comparison_path)

            # List ClearCase element path and version belonging to previous and
            # current labels, element path is the key of each dict.
            previous_elements = {}
            current_elements = {}
            previous_label_elements_thread = _GetElementsFromLabelThread(
                dir_name=comparison_path,
                label=previous_label,
                elements=previous_elements,
                vob_tags=matched_vobs)
            previous_label_elements_thread.start()

            current_label_elements_thread = _GetElementsFromLabelThread(
                dir_name=comparison_path,
                label=current_label,
                elements=current_elements,
                vob_tags=matched_vobs)
            current_label_elements_thread.start()

            previous_label_elements_thread.join()
            current_label_elements_thread.join()

            seen = set()
            changelist = {}

            # Iterate on each ClearCase path in order to find respective
            # previous and current version.
            for path in itertools.chain(previous_elements.keys(),
                                        current_elements.keys()):
                if path in seen:
                    continue

                seen.add(path)

                # Initialize previous and current version to '/main/0'
                main0 = f'{_MAIN}0'
                changelist[path] = {
                    'current': main0,
                    'previous': main0,
                }

                if path in current_elements:
                    changelist[path]['current'] = \
                        current_elements[path]['version']

                if path in previous_elements:
                    changelist[path]['previous'] = \
                        previous_elements[path]['version']

                # Prevent adding identical version to comparison.
                if changelist[path]['current'] == changelist[path]['previous']:
                    continue

                yield (
                    self._construct_extended_path(
                        path,
                        changelist[path]['previous']),
                    self._construct_extended_path(
                        path,
                        changelist[path]['current']),
                )
        except Exception as e:
            error_message = str(e)

            if error_message:
                raise SCMError('Label comparison failed:\n%s' % error_message)

    def _get_stream_changelist(
        self,
        stream: str,
        repository_info: ClearCaseRepositoryInfo,
    ) -> _ChangedEntryList:
        """Return information about the versions changed in a stream.

        Args:
            stream (str):
                The UCM stream name. This must include the PVOB tag as well, so
                that ``cleartool describe`` can fetch the branch name.

            repository_info (ClearCaseRepositoryInfo):
                The repository info structure.

        Returns:
            list:
            A list of the changed files.
        """
        stream_info = execute(
            [
                'cleartool',
                'describe',
                '-long',
                'stream:%s' % stream,
            ],
            split_lines=True)

        branch = None

        for line in stream_info:
            if line.startswith('  Guarding: brtype'):
                line_parts = line.strip().split(':', 2)
                branch = line_parts[2]
                break

        if not branch:
            logger.error('Unable to determine branch name for UCM stream %s',
                         stream)
            return []

        # TODO: It's possible that some project VOBs may exist in the stream
        # but not be included in the Review Board repository configuration. In
        # this case, _get_branch_changelist will only include changes in the
        # configured VOBs. There's also a possibility that some non-UCM or
        # other non-related UCM VOBs may have the same stream name or branch
        # name as the one being searched, and so it could include unexpected
        # versions. The chances of this in reality are probably pretty small.
        return self._get_branch_changelist(branch, repository_info)

    def _diff_directories(
        self,
        entry: _ChangesetEntry,
        repository_info: ClearCaseRepositoryInfo,
        diffx_change: DiffXChangeSection,
    ) -> bytes:
        """Return a unified diff for a changed directory.

        Args:
            entry (_ChangesetEntry):
                The changeset entry.

            repository_info (ClearCaseRepositoryInfo):
                The repository info structure.

            diffx_change (pydiffx.dom.DiffXChangeSection):
                The DiffX DOM object for writing VersionVault diffs.

        Returns:
            bytes:
            The diff between the two directory listings, for writing legacy
            ClearCase diffs.
        """
        diff_tool = self.get_diff_tool()
        assert diff_tool is not None

        old_path = entry.old_path
        assert old_path is not None

        old_content = self._get_directory_contents(old_path)
        old_tmp = make_tempfile(content=old_content)

        new_path = entry.new_path
        assert new_path is not None

        new_content = self._get_directory_contents(new_path)
        new_tmp = make_tempfile(content=new_content)

        # Diff the two files.
        diff_result = diff_tool.run_diff_file(orig_path=old_tmp,
                                              modified_path=new_tmp)

        stream = io.BytesIO()
        diff_writer = UnifiedDiffWriter(stream)

        if diff_result.has_text_differences:
            diff_writer.write_diff_file_result_headers(
                diff_result,
                orig_path=entry.old_path,
                modified_path=entry.new_path)

            if repository_info.is_legacy:
                diff_writer.write_line(
                    b'==== %s %s ===='
                    % (entry.old_oid.encode('utf-8'),
                       entry.new_oid.encode('utf-8')))

            diff_writer.write_diff_file_result_hunks(diff_result)

        diff_contents = stream.getvalue()

        if not repository_info.is_legacy:
            vv_metadata: dict[str, Any] = {
                'directory-diff': 'legacy-filenames',
                'vob': entry.vob_oid,
            }

            if entry.op == 'create':
                assert entry.new_path

                path = os.path.relpath(entry.new_path, self.root_path)
                revision = {
                    'new': entry.new_version,
                }
                vv_metadata['new'] = {
                    'name': entry.new_name,
                    'oid': entry.new_oid,
                    'path': path,
                }
            elif entry.op == 'delete':
                assert entry.old_path

                path = os.path.relpath(entry.old_path, self.root_path)
                revision = {
                    'old': entry.old_version,
                }
                vv_metadata['old'] = {
                    'name': entry.old_name,
                    'oid': entry.old_oid,
                    'path': path,
                }
            elif entry.op in ('modify', 'move'):
                assert entry.old_path
                assert entry.new_path

                old_path_rel = os.path.relpath(entry.old_path, self.root_path)
                new_path_rel = os.path.relpath(entry.new_path, self.root_path)

                path = {
                    'old': old_path_rel,
                    'new': new_path_rel,
                }
                revision = {
                    'old': entry.old_version,
                    'new': entry.new_version,
                }
                vv_metadata['old'] = {
                    'name': entry.old_name,
                    'oid': entry.old_oid,
                    'path': old_path_rel,
                }
                vv_metadata['new'] = {
                    'name': entry.new_name,
                    'oid': entry.new_oid,
                    'path': new_path_rel,
                }
            else:
                logger.warning(
                    'Unexpected operation "%s" for directory %s %s',
                    entry.op, entry.old_path, entry.new_path)
                return b''

            diffx_change.add_file(
                meta={
                    'op': entry.op,
                    'path': path,
                    'revision': revision,
                    'type': 'directory',
                    'versionvault': vv_metadata,
                },
                diff_type='text',
                diff=diff_contents)

        return diff_contents

    def _get_directory_contents(
        self,
        extended_path: str,
    ) -> bytes:
        """Return an ls-style directory listing for a versioned directory.

        Args:
            extended_path (str):
                The path of the directory to get the contents for.

        Returns:
            bytes:
            The contents of the directory.
        """
        output = execute(['cleartool', 'ls', '-short', '-nxname', '-vob_only',
                          extended_path],
                         split_lines=True,
                         results_unicode=False)

        contents = sorted(
            os.path.basename(absolute_path.strip())
            for absolute_path in output
        )

        # Add one extra empty line so the data passed to diff ends in a
        # newline.
        contents.append(b'')

        return b'\n'.join(contents)

    def _diff_files(
        self,
        entry: _ChangesetEntry,
        repository_info: ClearCaseRepositoryInfo,
        diffx_change: DiffXChangeSection,
    ) -> bytes:
        """Return a unified diff for a changed file.

        Args:
            entry (_ChangesetEntry):
                The changeset entry.

            repository_info (ClearCaseRepositoryInfo):
                The repository info structure.

            diffx_change (pydiffx.dom.DiffXChangeSection):
                The DiffX DOM object for writing VersionVault diffs.

        Returns:
            bytes:
            The diff between the two files, for writing legacy ClearCase diffs.
        """
        diff_tool = self.get_diff_tool()
        assert diff_tool is not None

        if entry.old_path:
            old_file_rel = os.path.relpath(entry.old_path, self.root_path)

            if repository_info.is_legacy:
                old_file_rel = os.path.join(repository_info.vobtag,
                                            old_file_rel)
        else:
            old_file_rel = '/dev/null'

        if entry.new_path:
            new_file_rel = os.path.relpath(entry.new_path, self.root_path)

            if repository_info.is_legacy:
                new_file_rel = os.path.join(repository_info.vobtag,
                                            new_file_rel)
        else:
            new_file_rel = '/dev/null'

        if self.viewtype == 'snapshot':
            # For snapshot views, we have to explicitly query to get the file
            # content and store in temporary files.
            try:
                old_path = entry.old_path
                assert old_path is not None

                new_path = entry.new_path
                assert new_path is not None

                diff_old_file = self._get_content_snapshot(old_path)
                diff_new_file = self._get_content_snapshot(new_path)
            except Exception as e:
                logger.exception(e)
                return b''
        else:
            # Dynamic views can access any version in history, but we may have
            # to create empty temporary files to compare against in the case of
            # created or deleted files.
            diff_old_file = entry.old_path or make_tempfile()
            diff_new_file = entry.new_path or make_tempfile()

        diff_result = diff_tool.run_diff_file(orig_path=diff_old_file,
                                              modified_path=diff_new_file)

        stream = io.BytesIO()
        diff_writer = UnifiedDiffWriter(stream)

        if diff_result.has_text_differences:
            # Replace temporary filenames in the diff with view-local relative
            # paths.
            diff_writer.write_diff_file_result_headers(
                diff_result,
                orig_path=old_file_rel,
                modified_path=new_file_rel)

        if diff_result.has_differences:
            if repository_info.is_legacy:
                diff_writer.write_line(
                    b'==== %s %s ===='
                    % (entry.old_oid.encode('utf-8'),
                       entry.new_oid.encode('utf-8')))

            diff_writer.write_diff_file_result_hunks(diff_result)

        diff_contents = stream.getvalue()

        if not repository_info.is_legacy:
            # We need oids of files to translate them to paths on reviewboard
            # repository.
            vob_oid = execute(['cleartool', 'describe', '-fmt', '%On',
                               f'vob:{entry.new_path or entry.old_path}'])

            vv_metadata = {
                'vob': vob_oid,
            }

            if diff_result.is_binary:
                diff_type = 'binary'
            else:
                diff_type = 'text'

            if entry.op == 'create':
                revision = entry.new_version

                path = new_file_rel
                revision = {
                    'new': revision,
                }
                vv_metadata['new'] = {
                    'name': entry.new_name,
                    'path': path,
                    'oid': entry.new_oid,
                }
            elif entry.op == 'delete':
                revision = entry.old_version

                path = old_file_rel
                revision = {
                    'old': revision,
                }
                vv_metadata['old'] = {
                    'name': entry.old_name,
                    'path': path,
                    'oid': entry.old_oid,
                }
            elif entry.op in ('modify', 'move'):
                path = {
                    'old': old_file_rel,
                    'new': new_file_rel,
                }
                revision = {
                    'old': entry.old_version,
                    'new': entry.new_version,
                }
                vv_metadata['old'] = {
                    'name': entry.old_name,
                    'path': old_file_rel,
                    'oid': entry.old_oid,
                }
                vv_metadata['new'] = {
                    'name': entry.new_name,
                    'path': new_file_rel,
                    'oid': entry.new_oid,
                }

                if entry.op == 'move' and diff_contents:
                    entry.op = 'move-modify'
            else:
                logger.warning('Unexpected operation "%s" for file %s %s',
                               entry.op, entry.old_path, entry.new_path)
                return b''

            diffx_change.add_file(
                meta={
                    'versionvault': vv_metadata,
                    'path': path,
                    'op': entry.op,
                    'revision': revision,
                    'type': 'file',
                },
                diff_type=diff_type,
                diff=diff_contents)

        return diff_contents

    def _get_content_snapshot(
        self,
        filename: str,
    ) -> str:
        """Return the content of a file in a snapshot view.

        Snapshot views don't support accessing file content directly like
        dynamic views do, so we have to fetch the content to a temporary file.

        Args:
            filename (str):
                The extended path of the file element to fetch.

        Returns:
            str:
            The filename of the temporary file with the content.
        """
        temp_file = make_tempfile()

        if filename:
            # Delete the temporary file so cleartool can write to it.
            try:
                os.remove(temp_file)
            except OSError:
                pass

            execute(['cleartool', 'get', '-to', temp_file, filename])

        return temp_file

    def _do_diff(
        self,
        changelist: _ChangedEntryList,
        repository_info: ClearCaseRepositoryInfo,
        metadata: dict[str, Any],
    ) -> SCMClientDiffResult:
        """Generate a unified diff for all files in the given changeset.

        Args:
            changelist (list):
                A list of changes.

            repository_info (ClearCaseRepositoryInfo):
                The repository info structure.

            metadata (dict):
                Extra data to inject into the diff headers.

        Returns:
            rbtools.clients.base.scmclient.SCMClientDiffResult:
            The diff result.
        """
        # Sanitize all changesets of version 0 before processing
        changelist = self._sanitize_version_0_changeset(changelist)
        changeset = self._process_directory_changes(changelist)

        diffx = DiffX()
        diffx_change = diffx.add_change(meta={
            'versionvault': metadata,
        })
        legacy_diffs = io.BytesIO()

        logger.debug('Doing diff of changeset: %s', changeset)

        for entry in changeset:
            legacy_diff: bytes

            if entry.is_dir:
                legacy_diff = self._diff_directories(entry,
                                                     repository_info,
                                                     diffx_change)
            else:
                if (self.viewtype == 'snapshot' or
                    (entry.new_path is not None and
                     cpath.exists(entry.new_path))):
                    legacy_diff = self._diff_files(entry,
                                                   repository_info,
                                                   diffx_change)
                else:
                    logger.error(
                        'File %s does not exist or access is denied.',
                        entry.new_path)
                    continue

            if repository_info.is_legacy and legacy_diff:
                legacy_diffs.write(legacy_diff)

        if repository_info.is_legacy:
            diff = legacy_diffs.getvalue()
        else:
            diffx.generate_stats()
            diff = diffx.to_bytes()

        return {
            'diff': diff,
        }

    def _is_dir(
        self,
        path: str,
    ) -> bool:
        """Return whether a given path is a directory.

        Args:
            path (str):
                The path of the element to check.

        Returns:
            bool:
            ``True`` if the given element is a directory.
        """
        if self.viewtype == 'dynamic' and cpath.exists(path):
            return cpath.isdir(path)
        else:
            object_kind = execute(
                ['cleartool', 'describe', '-fmt', '%m', path])

            return object_kind.startswith('directory')

    def _process_directory_changes(
        self,
        changelist: _ChangedEntryList,
    ) -> list[_ChangesetEntry]:
        """Scan through the changeset and handle directory elements.

        Depending on how the changeset is created, it may include changes to
        directory elements. These cover things such as file renames or
        deletions which may or may not be already included in the changeset.

        This method will perform diffs for any directory-type elements,
        processing those and folding them back into the changeset for use
        later.

        Args:
            changelist (_ChangedEntryList):
                The list of changed elements (2-tuples of element versions to
                compare)

        Returns:
            list of _ChangesetEntry:
            The new changeset including adds, deletes, and moves.
        """
        files = []
        directories = []

        for old_file, new_file in changelist:
            if self._is_dir(new_file):
                directories.append((old_file, new_file))
                files.append(_ChangesetEntry(root_path=self.root_path,
                                             old_path=old_file,
                                             new_path=new_file,
                                             is_dir=True))
            else:
                files.append(_ChangesetEntry(root_path=self.root_path,
                                             old_path=old_file,
                                             new_path=new_file))

        for old_dir, new_dir in directories:
            changes = self._get_file_changes_from_directories(old_dir, new_dir)

            for filename, oid in changes['added']:
                for file in files:
                    if file.new_oid == oid:
                        file.op = 'create'
                        break
                else:
                    if not self._is_dir(filename):
                        files.append(_ChangesetEntry(root_path=self.root_path,
                                                     new_path=filename,
                                                     new_oid=oid,
                                                     op='create'))

            for filename, oid in changes['deleted']:
                for file in files:
                    if file.old_oid == oid:
                        file.op = 'delete'
                        break
                else:
                    if not self._is_dir(filename):
                        # The extended path we get here doesn't include the
                        # revision of the element. While many operations can
                        # succeed in this case, fetching the content of the
                        # file from snapshot views does not. We therefore
                        # look at the history of the file and get the last
                        # revision from it.
                        filename = execute(['cleartool', 'lshistory', '-last',
                                            '1', '-fmt', '%Xn', f'oid:{oid}'])
                        files.append(_ChangesetEntry(root_path=self.root_path,
                                                     old_path=filename,
                                                     old_oid=oid,
                                                     op='delete'))

            for old_file, old_oid, new_file, new_oid in changes['renamed']:
                # Just using the old filename that we get from the
                # directory diff will break in odd ways depending on
                # the view type. Explicitly appending the element
                # version seems to work.

                for file in files:
                    if (file.old_oid == old_oid or
                        file.new_oid == new_oid):
                        old_version = execute(['cleartool', 'describe',
                                               '-fmt', '%Vn', file.old_path])
                        file.old_path = f'{old_file}@@{old_version}'
                        file.op = 'move'

                        break
                else:
                    if not self._is_dir(new_file):
                        files.append(_ChangesetEntry(root_path=self.root_path,
                                                     old_path=old_file,
                                                     new_path=new_file,
                                                     old_oid=old_oid,
                                                     new_oid=new_oid,
                                                     op='move'))

        return files

    def _get_file_changes_from_directories(
        self,
        old_dir: str,
        new_dir: str,
    ) -> DirectoryDiff:
        """Get directory differences.

        This will query and parse the diff of a directory element, in order to
        properly detect added, renamed, and deleted files.

        Args:
            old_dir (str):
                The extended path of the directory at its old revision.

            new_dir (str):
                The extended path of the directory at its new revision.

        Returns:
            dict:
            A dictionary with three keys: ``renamed``, ``added``, and
            ``deleted``.
        """
        diff_lines = execute(
            [
                'cleartool',
                'diff',
                '-ser',
                old_dir,
                new_dir,
            ],
            split_lines=True,
            extra_ignore_errors=(1,))

        current_mode = None
        mode_re = re.compile(r'^-----\[ (?P<mode>[\w ]+) \]-----$')

        def _extract_filename(fileline: str) -> str:
            return fileline.rsplit(None, 2)[0][2:]

        i = 0
        results: DirectoryDiff = {
            'added': set(),
            'deleted': set(),
            'renamed': set(),
        }

        while i < len(diff_lines):
            line = diff_lines[i]
            i += 1

            m = mode_re.match(line)

            if m:
                current_mode = m.group('mode')
                continue

            get_oid_cmd = ['cleartool', 'desc', '-fmt', '%On']

            try:
                if current_mode == 'renamed to':
                    old_file = cpath.join(old_dir, _extract_filename(line))
                    old_oid = execute(get_oid_cmd + [old_file])
                    new_file = cpath.join(new_dir,
                                          _extract_filename(diff_lines[i + 1]))
                    new_oid = execute(get_oid_cmd + [new_file])

                    results['renamed'].add(
                        (old_file, old_oid, new_file, new_oid))
                    i += 2
                elif current_mode == 'added':
                    new_file = cpath.join(new_dir, _extract_filename(line))
                    oid = execute(get_oid_cmd + [new_file])

                    results['added'].add((new_file, oid))
                elif current_mode == 'deleted':
                    old_file = cpath.join(old_dir, _extract_filename(line))
                    oid = execute(get_oid_cmd + [old_file])

                    results['deleted'].add((old_file, oid))
            except Exception as e:
                # It's possible that we'll get errors when trying to use
                # get_oid_cmd in some cases, such as when a symbolic link is
                # added or removed. In this cases, we'll just log a warning
                # and skip them for this step. We'll still show it when the
                # directory contents get diffed later.
                logger.debug('Got error while processing directory changes '
                             'from %s to %s: %s',
                             old_dir,
                             new_dir,
                             e)

        return results

    def _get_diff_metadata(
        self,
        revisions: SCMClientRevisionSpec,
    ) -> dict[str, Any]:
        """Return a starting set of metadata to inject into the diff.

        Args:
            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

        Returns:
            dict:
            A starting set of data to inject into the diff, which will become
            part of the FileDiff's extra_data field. Additional keys may be set
            on this before it gets serialized into the diff.
        """
        host_properties = self.host_properties
        assert host_properties is not None

        metadata = {
            'os': {
                'short': os.name,
                'long': host_properties.get('Operating system'),
            },
            'region': host_properties.get('Registry region'),
            'scm': {
                'name': host_properties.get('Product name'),
                'version': host_properties.get('Product version'),
            },
            'view': {
                'tag': self.viewname,
                'type': self.viewtype,
                'ucm': self.is_ucm,
            },
        }

        base = revisions['base']
        tip = revisions['tip']

        if tip == self.REVISION_CHECKEDOUT_CHANGESET:
            metadata['scope'] = {
                'name': 'checkout',
                'type': 'checkout',
            }
        elif base == self.REVISION_ACTIVITY_BASE:
            metadata['scope'] = {
                'name': tip,
                'type': 'activity',
            }
        elif base == self.REVISION_BASELINE_BASE:
            assert isinstance(tip, list)

            if len(tip) == 1:
                metadata['scope'] = {
                    'name': tip[0],
                    'type': 'baseline/predecessor',
                }
            else:
                metadata['scope'] = {
                    'name': f'{tip[0]}/{tip[1]}',
                    'type': 'baseline/baseline',
                }
        elif base == self.REVISION_BRANCH_BASE:
            metadata['scope'] = {
                'name': tip,
                'type': 'branch',
            }
        elif base == self.REVISION_LABEL_BASE:
            assert isinstance(tip, list)

            if len(tip) == 1:
                metadata['scope'] = {
                    'name': tip[0],
                    'type': 'label/current',
                }
            else:
                metadata['scope'] = {
                    'name': f'{tip[0]}/{tip[1]}',
                    'type': 'label/label',
                }
        elif base == self.REVISION_STREAM_BASE:
            metadata['scope'] = {
                'name': tip,
                'type': 'stream',
            }
        elif base == self.REVISION_FILES:
            # TODO: We'd like to keep a record of the individual files listed
            # in "tip"
            metadata['scope'] = {
                'name': 'changeset',
                'type': 'changeset',
            }
        else:
            assert False

        return metadata

    def _get_host_info(self) -> _HostProperties:
        """Return the current ClearCase/VersionVault host info.

        Returns:
            dict:
            A dictionary with the host properties.

        Raises:
            rbtools.clients.errors.SCMError:
                Could not determine the host info.
        """
        # NOTE: This can be removed once check_dependencies() is mandatory.
        if not self.has_dependencies(expect_checked=True):
            logger.debug('Unable to execute "cleartool help": skipping '
                         'ClearCase')
            return None

        property_lines = execute(['cleartool', 'hostinfo', '-l'],
                                 split_lines=True)

        if 'Error' in property_lines:
            raise SCMError('Unable to determine the current region')

        properties = {}

        for line in property_lines:
            key, value = line.split(':', 1)
            properties[key.strip()] = value.strip()

        # Add derived properties
        try:
            product = properties['Product'].split(' ', 1)
            properties['Product name'] = product[0]
            properties['Product version'] = product[1]
        except Exception:
            pass

        return properties


class ClearCaseRepositoryInfo(RepositoryInfo):
    """A representation of a ClearCase source code repository.

    This version knows how to find a matching repository on the server even if
    the URLs differ.
    """

    #: Whether the server uses the legacy ClearCase SCMTool.
    #:
    #: Type:
    #:     bool
    is_legacy: bool

    #: The SCM client.
    #:
    #: Type:
    #:     ClearCaseClient
    tool: ClearCaseClient

    #: A mapping from VOB UUID to matching VOB tags.
    #:
    #: Type:
    #:     dict
    uuid_to_tags: dict[str, list[str]]

    #: The set of VOB tags that the server has registered.
    #:
    #: Type:
    #:     set of str
    vob_tags: set[str]

    #: A list of the VOB UUIDs that the server has registered.
    #:
    #: Type:
    #:     list of str
    vob_uuids: list[str]

    def __init__(
        self,
        path: str,
        vobtag: str,
    ) -> None:
        """Initialize the repsitory info.

        Args:
            path (str):
                The path of the repository.

            vobtag (str):
                The VOB tag for the repository.
        """
        super().__init__(path=path)
        self.vobtag = vobtag
        self.vob_tags = {vobtag}
        self.uuid_to_tags = {}
        self.is_legacy = True

    def update_from_remote(
        self,
        repository: ItemResource,
        info: ItemResource,
    ) -> None:
        """Update the info from a remote repository.

        Args:
            repository (rbtools.api.resource.ItemResource):
                The repository resource.

            info (rbtools.api.resource.ItemResource):
                The repository info resource.
        """
        path = cast(str, info['repopath'])
        self.path = path

        if 'uuid' in info:
            # Legacy ClearCase backend that supports a single VOB.
            self.vob_uuids = cast(List[str], [info['uuid']])
        elif 'uuids' in info:
            # New VersionVault/ClearCase backend that supports multiple VOBs.
            self.vob_uuids = cast(List[str], info['uuids'])
            self.is_legacy = False
        else:
            raise SCMError('Unable to fetch VOB information from server '
                           'repository info.')

        tags = defaultdict(set)
        regions = cast(
            List[str],
            execute(['cleartool', 'lsregion'],
                    ignore_errors=True,
                    split_lines=True))

        # Find local tag names for connected VOB UUIDs.
        for region, uuid in itertools.product(regions, self.vob_uuids):
            try:
                tag = execute(['cleartool', 'lsvob', '-s', '-family', uuid,
                               '-region', region.strip()])
                tags[uuid].add(tag.strip())
            except Exception:
                pass

        self.vob_tags = set()
        self.uuid_to_tags = {}

        for uuid, tags in tags.items():
            self.vob_tags.update(tags)
            self.uuid_to_tags[uuid] = list(tags)

        if self.is_legacy:
            self.base_path = self.vobtag
