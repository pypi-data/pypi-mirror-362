"""A client for Mercurial."""

from __future__ import annotations

import logging
import os
import re
import uuid
from contextlib import ExitStack
from gettext import gettext as _
from typing import (Any, Iterator, Optional, Sequence, TYPE_CHECKING, Union,
                    cast)
from urllib.parse import urlsplit, urlunparse

from housekeeping import deprecate_non_keyword_only_args

from rbtools.clients import RepositoryInfo
from rbtools.clients.base.scmclient import (BaseSCMClient,
                                            SCMClientCommitHistoryItem,
                                            SCMClientDiffResult,
                                            SCMClientPatcher,
                                            SCMClientRevisionSpec)
from rbtools.clients.errors import (CreateCommitError,
                                    InvalidRevisionSpecError,
                                    MergeError,
                                    SCMClientDependencyError,
                                    SCMError,
                                    TooManyRevisionsError)
from rbtools.clients.svn import SVNClient
from rbtools.deprecation import RemovedInRBTools60Warning
from rbtools.diffs.errors import ApplyPatchError
from rbtools.diffs.patches import PatchAuthor, PatchResult
from rbtools.utils.checks import check_install
from rbtools.utils.console import edit_file
from rbtools.utils.encoding import force_unicode
from rbtools.utils.errors import EditorError
from rbtools.utils.filesystem import make_tempfile
from rbtools.utils.process import execute

if TYPE_CHECKING:
    from urllib.parse import SplitResult

    from rbtools.diffs.patches import Patch


logger = logging.getLogger(__name__)


class MercurialRefType:
    """Types of references in Mercurial."""

    #: Revision hashes.
    REVISION = 'revision'

    #: Branch names.
    BRANCH = 'branch'

    #: Bookmark names.
    BOOKMARK = 'bookmark'

    #: Tag names.
    TAG = 'tag'

    #: Unknown references.
    UNKNOWN = 'unknown'


class MercurialPatcher(SCMClientPatcher):
    """A patcher that applies Mercurial patches to a tree.

    This applies patches using :command:`hg import` and to manually handle
    added and deleted empty files.

    The patcher supports tracking conflicts and partially-applied patches.

    Version Added:
        5.1
    """

    def apply_patches(self) -> Iterator[PatchResult]:
        """Internal function to apply the patches.

        If applying files without committing, we'll open all the files and
        apply in one :command:`hg import` operation, helping Mercurial apply
        them correctly and without triggering an "uncommitted changes" error.

        If we're applying while committing, we'll use the default Patcher
        logic to apply and commit them one-by-one.

        Yields:
            rbtools.diffs.patches.PatchResult:
            The result of each patch application, whether the patch applied
            successfully or with normal patch failures.

        Raises:
            rbtools.diffs.errors.ApplyPatchResult:
                There was an error attempting to apply a patch.

                This won't be raised simply for conflicts or normal patch
                failures. It may be raised for errors encountered during
                the patching process.
        """
        if self.revert:
            raise ApplyPatchError(
                'Mercurial does not support reverting patches.',
                patcher=self)

        if self.squash:
            raise ApplyPatchError(
                'Mercurial does not support squashing patches.',
                patcher=self)

        if self.commit:
            # We're going to process these one-by-one, so that we can use
            # the generated or provided commit messages and author
            # information.
            yield from super().apply_patches()
        else:
            # We're going to apply all these in one go. We can't do these
            # one-by-one since Mercurial won't let us apply patches to a
            # dirty tree, and the tree will always be dirty after the first
            # patch.
            patches = self.patches
            prefix_level = patches[0].prefix_level

            # Open all patches at once so we can get filenames to apply.
            with ExitStack() as stack:
                filenames: list[str] = []

                for patch in patches:
                    stack.enter_context(patch.open())

                    if patch.prefix_level != prefix_level:
                        raise ApplyPatchError(
                            'Mercurial does not support applying multiple '
                            'patches with different --strip levels.',
                            patcher=self)

                    filenames.append(str(patch.path))

                if len(patches) == 1:
                    result_patch = patches[0]
                else:
                    result_patch = None

                yield self._run_hg_import(filenames=filenames,
                                          patch=result_patch,
                                          prefix_level=prefix_level,
                                          patch_range=(1, len(patches)))

    def apply_single_patch(
        self,
        *,
        patch: Patch,
        patch_num: int,
    ) -> PatchResult:
        """Internal function to apply a single patch.

        This will take a single patch and apply it using Subversion.

        Args:
            patch (rbtools.diffs.patches.Patch):
                The patch to apply, opened for reading.

            patch_num (int):
                The 1-based index of this patch in the full list of patches.

        Returns:
            rbtools.diffs.patches.PatchResult:
            The result of the patch application, whether the patch applied
            successfully or with normal patch failures.
        """
        return self._run_hg_import(filenames=[str(patch.path)],
                                   prefix_level=patch.prefix_level,
                                   patch=patch,
                                   patch_range=(patch_num, patch_num))

    def _run_hg_import(
        self,
        *,
        filenames: Sequence[str],
        prefix_level: Optional[int],
        patch: Optional[Patch],
        patch_range: tuple[int, int],
    ) -> PatchResult:
        """Run hg import and return a result.

        This will run :command:`hg import` in a non-commit mode, taking a list
        of files and applying them to the local tree.

        Args:
            filenames (list of str):
                The list of patch filenames to apply.

            prefix_level (int):
                The number of path components to strip from each path in the
                patch files.

            patch (rbtools.diffs.patches.Patch):
                The optional patch to associate with a result.

            patch_range (tuple):
                The patch range to associate with a result.

        Returns:
            rbtools.diffs.patches.PatchResult:
            The result from the patch operation.
        """
        scmclient = self.scmclient

        # For Mercurial, if we apply + commit, then we're going to commit in a
        # separate step instead of letting `hg import` do it. This lets us
        # handle our standard open-editor logic, data normalization, and error
        # handling without duplicating all that here, in exchange for one extra
        # call per patch.
        #
        # We are going to apply failing commits partially, since users will
        # have conflict and reject information to work from.
        cmd: list[str] = [scmclient._exe, 'import', '--no-commit', '--partial']

        if prefix_level is not None:
            cmd += ['-p', str(prefix_level)]

        cmd += filenames

        rc, patch_output = scmclient._execute(cmd,
                                              with_errors=True,
                                              return_error_code=True,
                                              ignore_errors=True,
                                              results_unicode=False)

        conflicting_files: list[str] = []
        applied: bool

        if rc == 0:
            applied = True
        else:
            parsed_output = self.parse_patch_output(patch_output)

            if parsed_output.get('fatal_error'):
                raise ApplyPatchError(
                    _('There was an error applying %%(patch_subject)s: '
                      '%(error)s')
                    % {
                        'error': force_unicode(patch_output).strip(),
                    },
                    patcher=self,
                    failed_patch_result=PatchResult(
                        applied=False,
                        patch=patch,
                        patch_output=patch_output,
                        patch_range=patch_range))

            conflicting_files = parsed_output['conflicting_files']
            applied = parsed_output['has_partial_applied_files']

        # We're done here. Send the result.
        return PatchResult(
            applied=applied,
            patch=patch,
            patch_output=patch_output,
            patch_range=patch_range,
            has_conflicts=len(conflicting_files) > 0,
            conflicting_files=conflicting_files)


class MercurialClient(BaseSCMClient):
    """A client for Mercurial.

    This is a wrapper around the hg executable that fetches repository
    information and generates compatible diffs.
    """

    scmclient_id = 'mercurial'
    name = 'Mercurial'
    server_tool_names = 'Mercurial,Subversion'
    server_tool_ids = ['mercurial', 'subversion']

    patcher_cls = MercurialPatcher

    supports_commit_history = True
    supports_diff_exclude_patterns = True
    supports_parent_diffs = True
    can_bookmark = True
    can_branch = True
    can_get_file_content = True
    can_merge = True

    NO_PARENT = '0' * 40

    # The ASCII field separator.
    _FIELD_SEP = '\x1f'

    # The ASCII field separator as an escape sequence.
    #
    # This is passed to Mercurial, where it is interpreted and transformed into
    # the actual character.
    _FIELD_SEP_ESC = r'\x1f'

    # The ASCII record separator.
    _RECORD_SEP = '\x1e'

    # The ASCII record separator as an escape sequence.
    #
    # This is passed to Mercurial, where it is interpreted and transformed into
    # the actual character.
    _RECORD_SEP_ESC = r'\x1e'

    ######################
    # Instance variables #
    ######################

    #: The loaded .hgrc content.
    hgrc: dict[str, Any]

    #: The executable to use for invoking hg.
    _exe: str

    #: The type of the hg backend (either "hg" or "svn").
    _type: str

    #: Whether the tool has been initialized.
    _initted: bool

    #: The environment to use when invoking hg.
    _hg_env: dict[str, str]

    #: The path to the hgext helper.
    _hgext_path: str

    #: The path to the remote.
    _remote_path: list[str]

    #: Candidates to check to find the remote path.
    #:
    #: This is an ordered set of hgrc paths that are checked if the
    #: tracking option is not given # explicitly. The first candidate found
    #: to exist will be used, falling back to ``default`` (the last member.)
    _remote_path_candidates: list[str]

    @deprecate_non_keyword_only_args(RemovedInRBTools60Warning)
    def __init__(
        self,
        *,
        executable: str = 'hg',
        **kwargs,
    ) -> None:
        """Initialize the client.

        Args:
            executable (str, optional):
                The name of the Mercurial executable to use.

            **kwargs (dict):
                Keyword arguments to pass through to the superclass.
        """
        super().__init__(**kwargs)

        self.hgrc = {}
        self._exe = executable
        self._type = 'hg'
        self._remote_path = []
        self._initted = False
        self._hg_env = {
            'HGPLAIN': '1',
        }

        self._hgext_path = os.path.normpath(os.path.join(
            os.path.dirname(__file__),
            '..', 'helpers', 'hgext.py'))

        self._remote_path_candidates = ['reviewboard', 'origin', 'parent',
                                        'default']

    def check_dependencies(self) -> None:
        """Check whether all base dependencies are available.

        This checks for the presence of :command:`hg` (or whichever executable
        is passed in to the client's constructor) in the system path.

        Version Added:
            4.0

        Raises:
            rbtools.clients.errors.SCMClientDependencyError:
                A :command:`hg` tool could not be found.
        """
        if not check_install([self._exe, '--help']):
            raise SCMClientDependencyError(missing_exes=[self._exe])

    @property
    def hidden_changesets_supported(self) -> bool:
        """Return whether the repository supports hidden changesets.

        Mercurial 1.9 and above support hidden changesets. These are changesets
        that have been hidden from regular repository view. They still exist
        and are accessible, but only if the --hidden command argument is
        specified.

        Since we may encounter hidden changesets (e.g. the user specifies
        hidden changesets as part of the revision spec), we need to be aware
        of hidden changesets.

        Type:
            bool
        """
        if not hasattr(self, '_hidden_changesets_supported'):
            # The choice of command is arbitrary. parents for the initial
            # revision should be fast.
            #
            # Note that this cannot use self._execute, as this property is
            # accessed by that function, and we don't want to infinitely
            # recurse.
            result = execute(
                [self._exe, 'parents', '--hidden', '-r', '0'],
                ignore_errors=True,
                with_errors=False,
                none_on_ignored_error=True)
            self._hidden_changesets_supported = result is not None

        return self._hidden_changesets_supported

    @property
    def hg_root(self) -> Optional[str]:
        """Return the root of the working directory.

        This will return the root directory of the current repository. If the
        current working directory is not inside a mercurial repository, this
        returns None.

        Type:
            str
        """
        if not hasattr(self, '_hg_root'):
            self._load_hgrc()

            key = 'bundle.mainreporoot'
            if key in self.hgrc:
                self._hg_root = self.hgrc[key]
            else:
                self._hg_root = None

        return self._hg_root

    def _init(self) -> None:
        """Initialize the client."""
        if self._initted or not self.hg_root:
            return

        if 'extensions.hgsubversion' in self.hgrc:
            svn_info = execute([self._exe, 'svn', 'info'],
                               ignore_errors=True)
        else:
            svn_info = None

        if (svn_info and
            not svn_info.startswith('abort:') and
            'hg: unknown command' not in svn_info and
            not svn_info.lower().startswith('not a child of')):
            self._type = 'svn'
            self._svn_info = svn_info
        else:
            self._type = 'hg'

            for candidate in self._remote_path_candidates:
                rc_key = 'paths.%s' % candidate

                if rc_key in self.hgrc:
                    self._remote_path = [candidate, self.hgrc[rc_key]]
                    logging.debug('Using candidate path %r: %r',
                                  self._remote_path[0], self._remote_path[1])
                    break

        self._initted = True

    def get_commit_history(
        self,
        revisions: SCMClientRevisionSpec,
    ) -> Optional[list[SCMClientCommitHistoryItem]]:
        """Return the commit history specified by the revisions.

        Args:
            revisions (dict):
                A dictionary of revisions to generate history for, as returned
                by :py:meth:`parse_revision_spec`.

        Returns:
            list of dict:
            This list of history entries, in order.

        Raises:
            rbtools.clients.errors.SCMError:
                The history is non-linear or there is a commit with no parents.
        """
        log_fields = {
            'commit_id': '{node}',
            'parent_id': '{p1node}',
            'author_name': '{author|person}',
            'author_email': '{author|email}',
            'author_date': '{date|rfc3339date}',
            'parent2': '{p2node}',
            'commit_message': '{desc}',
        }
        log_format = self._FIELD_SEP_ESC.join(log_fields.values())

        log_entries = self._execute(
            [
                self._exe,
                'log',
                '--template',
                f'{log_format}{self._RECORD_SEP_ESC}',
                '-r',
                '%(base)s::%(tip)s and not %(base)s' % revisions,
            ],
            ignore_errors=True,
            none_on_ignored_error=True,
            results_unicode=True)

        if not log_entries:
            return None

        history = []
        field_names = log_fields.keys()

        # The ASCII record separator will be appended to every record, so if we
        # attempt to split the entire output by the record separator, we will
        # end up with an empty ``log_entry`` at the end, which will cause
        # errors.
        for log_entry in log_entries[:-1].split(self._RECORD_SEP):
            fields = log_entry.split(self._FIELD_SEP)
            entry = dict(zip(field_names, fields))

            # We do not want `parent2` to be included in the entry because
            # the entry's items are used as the keyword arguments to the
            # method that uploads a commit and it would be unexpected.
            if entry.pop('parent2') != self.NO_PARENT:
                raise SCMError(
                    'The Mercurial SCMClient only supports posting commit '
                    'histories that are entirely linear.'
                )
            elif entry['parent_id'] == self.NO_PARENT:
                raise SCMError(
                    'The Mercurial SCMClient only supports posting commits '
                    'that have exactly one parent.'
                )

            history.append(entry)

        return history

    def get_local_path(self) -> Optional[str]:
        """Return the local path to the working tree.

        Returns:
            str:
            The filesystem path of the repository on the client system.
        """
        # NOTE: This can be removed once check_dependencies() is mandatory.
        if not self.has_dependencies(expect_checked=True):
            logging.debug('Unable to execute "hg --help": skipping Mercurial')
            return None

        return self.hg_root

    def get_repository_info(self) -> Optional[RepositoryInfo]:
        """Return repository information for the current working tree.

        Returns:
            rbtools.clients.base.repository.RepositoryInfo:
            The repository info structure.
        """
        # NOTE: This can be removed once check_dependencies() is mandatory.
        if not self.has_dependencies(expect_checked=True):
            logging.debug('Unable to execute "hg --help": skipping Mercurial')
            return None

        self._init()

        if not self.hg_root:
            # hg aborted => no mercurial repository here.
            return None

        if self._type == 'svn':
            return self._calculate_hgsubversion_repository_info(self._svn_info)
        else:
            path = self.hg_root
            base_path = '/'

            if self._remote_path:
                path = self._remote_path[1]
                base_path = ''

            return RepositoryInfo(path=path,
                                  base_path=base_path,
                                  local_path=self.hg_root)

    def parse_revision_spec(
        self,
        revisions: list[str] = [],
    ) -> SCMClientRevisionSpec:
        """Parse the given revision spec.

        These will be used to generate the diffs to upload to Review Board
        (or print). The diff for review will include the changes in (base,
        tip], and the parent diff (if necessary) will include (parent,
        base].

        If zero revisions are passed in, this will return the outgoing
        changes from the parent of the working directory.

        If a single revision is passed in, this will return the parent of
        that revision for "base" and the passed-in revision for "tip". This
        will result in generating a diff for the changeset specified.

        If two revisions are passed in, they will be used for the "base"
        and "tip" revisions, respectively.

        In all cases, a parent base will be calculated automatically from
        changesets not present on the remote.

        Args:
            revisions (list of str, optional):
                A list of revisions as specified by the user.

        Returns:
            dict:
            The parsed revision spec.

            See :py:class:`~rbtools.clients.base.scmclient.
            SCMClientRevisionSpec` for the format of this dictionary.

            This always populates ``base`` and ``tip``.

            ``commit_id`` and ``parent_base`` may also be populated.

        Raises:
            rbtools.clients.errors.InvalidRevisionSpecError:
                The given revisions could not be parsed.

            rbtools.clients.errors.TooManyRevisionsError:
                The specified revisions list contained too many revisions.
        """
        result: SCMClientRevisionSpec

        self._init()

        n_revisions = len(revisions)

        if n_revisions == 1:
            # If there's a single revision, try splitting it based on hg's
            # revision range syntax (either :: or ..). If this splits, then
            # it's handled as two revisions below.
            revisions = re.split(r'\.\.|::', revisions[0])
            n_revisions = len(revisions)

        if n_revisions == 0:
            # No revisions: Find the outgoing changes. Only consider the
            # working copy revision and ancestors because that makes sense.
            # If a user wishes to include other changesets, they can run
            # `hg up` or specify explicit revisions as command arguments.
            if self._type == 'svn':
                result = {
                    'base': self._get_parent_for_hgsubversion(),
                    'tip': '.',
                }
            else:
                # Ideally, generating a diff for outgoing changes would be as
                # simple as just running `hg outgoing --patch <remote>`, but
                # there are a couple problems with this. For one, the
                # server-side diff parser isn't equipped to filter out diff
                # headers such as "comparing with..." and
                # "changeset: <rev>:<hash>". Another problem is that the output
                # of `hg outgoing` potentially includes changesets across
                # multiple branches.
                #
                # In order to provide the most accurate comparison between
                # one's local clone and a given remote (something akin to git's
                # diff command syntax `git diff <treeish>..<treeish>`), we have
                # to do the following:
                #
                # - Get the name of the current branch
                # - Get a list of outgoing changesets, specifying a custom
                #   format
                # - Filter outgoing changesets by the current branch name
                # - Get the "top" and "bottom" outgoing changesets
                #
                # These changesets are then used as arguments to
                # `hg diff -r <rev> -r <rev>`.
                #
                # Future modifications may need to be made to account for odd
                # cases like having multiple diverged branches which share
                # partial history--or we can just punish developers for doing
                # such nonsense :)
                outgoing = \
                    self._get_bottom_and_top_outgoing_revs_for_remote(rev='.')

                if outgoing[0] is None or outgoing[1] is None:
                    raise InvalidRevisionSpecError(
                        'There are no outgoing changes')

                tip = self._identify_revision(outgoing[1])

                result = {
                    'base': self._identify_revision(outgoing[0]),
                    'commit_id': tip,
                    'tip': tip,
                }

                # Since the user asked us to operate on tip, warn them about a
                # dirty working directory.
                if (self.has_pending_changes() and
                    not self.config.get('SUPPRESS_CLIENT_WARNINGS', False)):
                    logging.warning('Your working directory is not clean. Any '
                                    'changes which have not been committed '
                                    'to a branch will not be included in your '
                                    'review request.')

            if self.options and self.options.parent_branch:
                result['parent_base'] = result['base']
                result['base'] = self._identify_revision(
                    self.options.parent_branch)
        elif n_revisions == 1:
            # One revision: Use the given revision for tip, and find its parent
            # for base.
            tip = self._identify_revision(revisions[0])
            base = self._execute(
                [self._exe, 'parents', '--hidden', '-r', tip,
                 '--template', '{node}']).split()[0]

            if len(base) != 40:
                raise InvalidRevisionSpecError(
                    "Can't determine parent revision")

            result = {
                'base': base,
                'commit_id': tip,
                'tip': tip,
            }
        elif n_revisions == 2:
            # Two revisions: Just use the given revisions
            result = {
                'base': self._identify_revision(revisions[0]),
                'tip': self._identify_revision(revisions[1]),
            }
        else:
            raise TooManyRevisionsError

        if self._type == 'hg' and 'parent_base' not in result:
            # If there are missing changesets between base and the remote, we
            # need to generate a parent diff.
            outgoing = self._get_outgoing_changesets(
                self._get_remote_branch(),
                rev=cast(str, result['base']))

            logging.debug('%d outgoing changesets between remote and base.',
                          len(outgoing))

            if not outgoing:
                return result

            parent_base = self._execute(
                [self._exe, 'parents', '--hidden', '-r', outgoing[0][1],
                 '--template', '{node}']).split()

            if len(parent_base) == 0:
                raise Exception(
                    'Could not find parent base revision. Ensure upstream '
                    'repository is not empty.')

            result['parent_base'] = parent_base[0]

            logging.debug('Identified %s as parent base',
                          result['parent_base'])

        return result

    def _identify_revision(
        self,
        revision: Union[str, int],
    ) -> str:
        """Identify the given revision.

        Args:
            revision (str or int):
                The revision.

        Raises:
            rbtools.clients.errors.InvalidRevisionSpecError:
                The specified revision could not be identified.

        Returns:
            str:
            The global revision ID of the commit.
        """
        identify = self._execute(
            [self._exe, 'identify', '-i', '--hidden',
             '--template', '{node}', '-r',
             str(revision)],
            ignore_errors=True, none_on_ignored_error=True)

        if identify is None:
            raise InvalidRevisionSpecError(
                '"%s" does not appear to be a valid revision' % revision)
        else:
            return identify.split()[0]

    def _calculate_hgsubversion_repository_info(
        self,
        svn_info: str,
    ) -> Optional[RepositoryInfo]:
        """Return repository info for an hgsubversion checkout.

        Args:
            svn_info (str):
                The SVN info output.

        Returns:
            rbtools.clients.base.repository.RepositoryInfo:
            The repository info structure, if available.
        """
        def _info(
            r: str,
        ) -> Optional[SplitResult]:
            m = re.search(r, svn_info, re.M)

            if m:
                return urlsplit(m.group(1))
            else:
                return None

        self._type = 'svn'

        root = _info(r'^Repository Root: (.+)$')
        url = _info(r'^URL: (.+)$')

        if not (root and url):
            return None

        scheme, netloc, path, _, _ = root
        root = urlunparse([scheme, root.netloc.split('@')[-1], path,
                           '', '', ''])
        base_path = url.path[len(path):]

        return RepositoryInfo(path=root,
                              base_path=base_path,
                              local_path=self.hg_root)

    def _load_hgrc(self) -> None:
        """Load the hgrc file."""
        for line in execute([self._exe, 'showconfig'],
                            env=self._hg_env,
                            with_errors=False,
                            split_lines=True):
            line = line.split('=', 1)

            if len(line) == 2:
                key, value = line
            else:
                key = line[0]
                value = ''

            self.hgrc[key] = value.strip()

    def get_hg_ref_type(
        self,
        ref: str,
    ) -> str:
        """Return the type of a reference in Mercurial.

        This can be used to determine if something is a bookmark, branch,
        tag, or revision.

        Args:
            ref (str):
                The reference to return the type for.

        Returns:
            str:
            The reference type. This will be a value in
            :py:class:`MercurialRefType`.
        """
        # Check for any bookmarks matching ref.
        rc, output = self._execute([self._exe, 'log', '-ql1', '-r',
                                    'bookmark(%s)' % ref],
                                   ignore_errors=True,
                                   return_error_code=True)

        if rc == 0:
            return MercurialRefType.BOOKMARK

        # Check for any bookmarks matching ref.
        #
        # Ideally, we'd use the same sort of log call we'd use for bookmarks
        # and tags, but it works differently for branches, and will
        # incorrectly match tags.
        branches = self._execute([self._exe, 'branches', '-q']).split()

        if ref in branches:
            return MercurialRefType.BRANCH

        # Check for any tags matching ref.
        rc, output = self._execute([self._exe, 'log', '-ql1', '-r',
                                    'tag(%s)' % ref],
                                   ignore_errors=True,
                                   return_error_code=True)

        if rc == 0:
            return MercurialRefType.TAG

        # Now just check that it exists at all. We'll assume it's a revision.
        rc, output = self._execute([self._exe, 'identify', '-r', ref],
                                   ignore_errors=True,
                                   return_error_code=True)

        if rc == 0:
            return MercurialRefType.REVISION

        return MercurialRefType.UNKNOWN

    def get_raw_commit_message(
        self,
        revisions: SCMClientRevisionSpec,
    ) -> str:
        """Return the raw commit message.

        This extracts all descriptions in the given revision range and
        concatenates them, most recent ones going first.

        Args:
            revisions (dict):
                A dictionary containing ``base`` and ``tip`` keys.

        Returns:
            str:
            The commit messages of all commits between (base, tip].
        """
        rev1 = revisions['base']
        rev2 = revisions['tip']

        delim = str(uuid.uuid1())
        descs = self._execute(
            [self._exe, 'log', '--hidden', '-r', f'{rev1}::{rev2}',
             '--template', '{desc}%s' % delim],
            env=self._hg_env)

        # This initial element in the base changeset, which we don't
        # care about. The last element is always empty due to the string
        # ending with <delim>.
        descs = descs.split(delim)[1:-1]

        return '\n\n'.join(desc.strip() for desc in descs)

    def diff(
        self,
        revisions: SCMClientRevisionSpec,
        *,
        include_files: list[str] = [],
        exclude_patterns: list[str] = [],
        with_parent_diff: bool = True,
        **kwargs,
    ) -> SCMClientDiffResult:
        """Perform a diff using the given revisions.

        This will generate a Git-style diff and parent diff (if needed) for
        the provided revisions. The diff will contain additional metadata
        headers used by Review Board to locate the appropriate revisions from
        the repository.

        Args:
            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            include_files (list of str, optional):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of str, optional):
                A list of shell-style glob patterns to blacklist during diff
                generation.

            with_parent_diff (bool, optional):
                Whether or not to include the parent diff in the result.

            **kwargs (dict, unused):
                Unused keyword arguments.

        Returns:
            dict:
            A dictionary containing keys documented in
            :py:class:`~rbtools.clients.base.scmclient.SCMClientDiffResult`.
        """
        self._init()

        diff_args = ['--hidden', '--nodates', '-g']

        if self._type == 'svn':
            diff_args.append('--svn')

        diff_args += include_files

        for pattern in exclude_patterns:
            diff_args += ['-X', pattern]

        node_base_id = cast(str, revisions['base'])

        diff = self._run_diff(diff_args,
                              parent_id=node_base_id,
                              node_id=cast(str, revisions['tip']))

        if with_parent_diff and 'parent_base' in revisions:
            base_commit_id = cast(str, revisions['parent_base'])
            parent_diff = self._run_diff(diff_args,
                                         parent_id=base_commit_id,
                                         node_id=node_base_id)
        else:
            base_commit_id = node_base_id
            parent_diff = None

        # If reviewboard requests a relative revision via hgweb it will fail
        # since hgweb does not support the relative revision syntax (^1, -1).
        # Rewrite this relative node id to an absolute node id.
        match = re.match(r'^[a-z|A-Z|0-9]*$', base_commit_id)

        if not match:
            base_commit_id = self._execute(
                [self._exe, 'log', '-r', base_commit_id,
                 '--template', '{node}'],
                env=self._hg_env, results_unicode=False)

        return {
            'diff': diff,
            'parent_diff': parent_diff,
            'commit_id': revisions.get('commit_id'),
            'base_commit_id': base_commit_id,
        }

    def _run_diff(
        self,
        diff_args: list[str],
        parent_id: str,
        node_id: str,
    ) -> bytes:
        """Run a diff command and normalize its results.

        This will run :command:`hg diff` with the provided arguments for the
        provided revision range, performing some normalization on the diff to
        prepare it for use in Review Board.

        Args:
            diff_args (list of str):
                The arguments to pass to :command:`hg diff` (except for any
                revision ranges).

            parent_id (str):
                The ID of the parent commit for the range.

            node_id (str):
                The ID of the latest commit for the range.

        Returns:
            bytes:
            The normalized diff content.
        """
        diff = self._execute(
            [self._exe, 'diff'] + diff_args + ['-r', parent_id, '-r', node_id],
            env=self._hg_env,
            log_output_on_error=False,
            results_unicode=False)

        return self._normalize_diff(diff,
                                    node_id=node_id,
                                    parent_id=parent_id)

    def _normalize_diff(
        self,
        diff: bytes,
        node_id: str,
        parent_id: str,
    ) -> bytes:
        """Normalize a diff, adding any headers that may be needed.

        For Git-style diffs, this will ensure the diff starts with information
        required for Review Board to identify the commit and its parent. These
        are based on headers normally generated by :command:`hg export`.

        Args:
            diff (bytes):
                The generated diff content to prepend to.

            node_id (str):
                The revision of this change.

            parent_id (str):
                The revision of the parent change.

        Returns:
            bytes:
            The normalized diff content.
        """
        assert isinstance(diff, bytes)

        if diff.lstrip().startswith(b'diff --git'):
            diff = (
                b'# HG changeset patch\n'
                b'# Node ID %(node_id)s\n'
                b'# Parent  %(parent_id)s\n'
                b'%(diff)s'
                % {
                    b'node_id': node_id.encode('utf-8'),
                    b'parent_id': parent_id.encode('utf-8'),
                    b'diff': diff,
                }
            )

        return diff

    def _get_files_in_changeset(
        self,
        rev: str,
    ) -> set[str]:
        """Return a set of all files in the specified changeset.

        Args:
            rev (str):
                A changeset identifier.

        Returns:
            set of str:
            A set of filenames in the changeset.
        """
        cmd = [self._exe, 'locate', '-r', rev]

        files = self._execute(cmd,
                              env=self._hg_env,
                              ignore_errors=True,
                              none_on_ignored_error=True)

        if files:
            files = files.replace('\\', '/')  # workaround for issue 3894

            return set(files.splitlines())

        return set()

    def _get_parent_for_hgsubversion(self) -> str:
        """Return the parent Subversion branch.

        Returns the parent branch defined in the command options if it exists,
        otherwise returns the parent Subversion branch of the current
        repository.

        Returns:
            str:
            The branch branch for the hgsubversion checkout.
        """
        return (
            getattr(self.options, 'tracking', None) or
            self._execute([
                self._exe, 'parent', '--svn', '--template', '{node}\n',
            ]).strip())

    def _get_remote_branch(self) -> str:
        """Return the remote branch associated with this repository.

        If the remote branch is not defined, the parent branch of the
        repository is returned.

        Returns:
            str:
            The name of the tracking branch.
        """
        remote = getattr(self.options, 'tracking', None)

        if not remote:
            try:
                remote = self._remote_path[0]
            except IndexError:
                remote = None

        if not remote:
            raise SCMError('Could not determine remote branch to use for '
                           'diff creation. Specify --tracking-branch to '
                           'continue.')

        return remote

    def create_commit(
        self,
        message: str,
        author: PatchAuthor,
        run_editor: bool,
        files: list[str] = [],
        all_files: bool = False,
    ) -> None:
        """Commit the given modified files.

        This is expected to be called after applying a patch. This commits the
        patch using information from the review request, opening the commit
        message in $EDITOR to allow the user to update it.

        Args:
            message (str):
                The commit message to use.

            author (rbtools.clients.base.scmclient.PatchAuthor):
                The author of the commit. This is expected to have ``fullname``
                and ``email`` attributes.

            run_editor (bool):
                Whether to run the user's editor on the commit message before
                committing.

            files (list of str, optional):
                The list of filenames to commit.

            all_files (bool, optional):
                Whether to commit all changed files, ignoring the ``files``
                argument.

        Raises:
            rbtools.clients.errors.CreateCommitError:
                The commit message could not be created. It may have been
                aborted by the user.
        """
        if run_editor:
            filename = make_tempfile(content=message.encode('utf-8'),
                                     prefix='hg-editor-',
                                     suffix='.txt')

            try:
                modified_message = edit_file(filename)
            except EditorError as e:
                raise CreateCommitError(str(e))
            finally:
                try:
                    os.unlink(filename)
                except OSError:
                    pass
        else:
            modified_message = message

        if not modified_message.strip():
            raise CreateCommitError(
                "A commit message wasn't provided. The patched files are in "
                "your tree but haven't been committed.")

        hg_command = [self._exe, 'commit', '-m', modified_message]

        try:
            hg_command += ['-u', f'{author.full_name} <{author.email}>']
        except AttributeError:
            # Users who have marked their profile as private won't include the
            # fullname or email fields in the API payload. Just commit as the
            # user running RBTools.
            logger.warning('The author has marked their Review Board profile '
                           'information as private. Committing without '
                           'author attribution.')

        if all_files:
            hg_command.append('-A')
        else:
            hg_command += files

        try:
            self._execute(hg_command)
        except Exception as e:
            raise CreateCommitError(str(e))

    def merge(
        self,
        target: str,
        destination: str,
        message: str,
        author: PatchAuthor,
        squash: bool = False,
        run_editor: bool = False,
        close_branch: bool = False,
        **kwargs,
    ) -> None:
        """Merge the target branch with destination branch.

        Args:
            target (str):
                The name of the branch to merge.

            destination (str):
                The name of the branch to merge into.

            message (str):
                The commit message to use.

            author (rbtools.clients.base.scmclient.PatchAuthor):
                The author of the commit. This is expected to have ``fullname``
                and ``email`` attributes.

            squash (bool, optional):
                Whether to squash the commits or do a plain merge. This is not
                used for Mercurial.

            run_editor (bool, optional):
                Whether to run the user's editor on the commit message before
                committing.

            close_branch (bool, optional):
                Whether to delete the branch after merging.

            **kwargs (dict, unused):
                Additional keyword arguments passed, for future expansion.

        Raises:
            rbtools.clients.errors.MergeError:
                An error occurred while merging the branch.
        """
        ref_type = self.get_hg_ref_type(target)

        if ref_type == MercurialRefType.UNKNOWN:
            raise MergeError('Could not find a valid branch, tag, bookmark, '
                             'or revision called "%s".'
                             % target)

        if close_branch and ref_type == MercurialRefType.BRANCH:
            try:
                self._execute([self._exe, 'update', target])
            except Exception as e:
                raise MergeError(
                    f'Could not switch to branch "{target}".\n\n{e}')

            try:
                self._execute([self._exe, 'commit', '-m', message,
                               '--close-branch'])
            except Exception as e:
                raise MergeError(
                    f'Could not close branch "{target}".\n\n{e}')

        try:
            self._execute([self._exe, 'update', destination])
        except Exception as e:
            raise MergeError(
                f'Could not switch to branch "{destination}".\n\n{e}')

        try:
            self._execute([self._exe, 'merge', target])
        except Exception as e:
            raise MergeError(
                f'Could not merge {ref_type} "{target}" into '
                f'"{destination}".\n\n{e}')

        self.create_commit(message=message,
                           author=author,
                           run_editor=run_editor)

        if close_branch and ref_type == MercurialRefType.BOOKMARK:
            try:
                self._execute([self._exe, 'bookmark', '-d', target])
            except Exception as e:
                raise MergeError(
                    f'Could not delete bookmark "{target}".\n\n{e}')

    def _get_current_branch(self) -> str:
        """Return the current branch of this repository.

        Returns:
            str:
            The name of the currently checked-out branch.
        """
        return self._execute([self._exe, 'branch'], env=self._hg_env).strip()

    def _get_bottom_and_top_outgoing_revs_for_remote(
        self,
        rev: Optional[str] = None,
    ) -> tuple[Optional[int], Optional[int]]:
        """Return the bottom and top outgoing revisions.

        Args:
            rev (str, optional):
                An optional revision to limit the results. If specified, only
                outgoing changesets which are ancestors of this revision will
                be included.

        Returns:
            tuple:
            A 2-tuple containing the bottom and top outgoing revisions for the
            changesets between the current branch and the remote branch.
        """
        remote = self._get_remote_branch()
        current_branch = self._get_current_branch()

        outgoing = [o for o in self._get_outgoing_changesets(remote, rev=rev)
                    if current_branch == o[2]]

        if outgoing:
            top_rev, bottom_rev = \
                self._get_top_and_bottom_outgoing_revs(outgoing)
        else:
            top_rev = None
            bottom_rev = None

        return bottom_rev, top_rev

    def _get_outgoing_changesets(
        self,
        remote: str,
        rev: Optional[str] = None,
    ) -> list[tuple[int, str, str]]:
        """Return the outgoing changesets between us and a remote.

        Args:
            remote (str):
                The name of the remote.

            rev (str, optional):
                An optional revision to limit the results. If specified, only
                outgoing changesets which are ancestors of this revision will
                be included.

        Returns:
            list:
            A list of tuples, each containing ``(rev, node, branch)``, for each
            outgoing changeset. The list will be sorted in revision order.
        """
        outgoing_changesets = []

        args = [
            self._exe, '-q', 'outgoing', '--template',
            '{rev}\\t{node}\\t{branch}\\n', remote,
        ]

        if rev:
            args += ['-r', rev]

        # We must handle the special case where there are no outgoing commits
        # as mercurial has a non-zero return value in this case.
        raw_outgoing = self._execute(args,
                                     env=self._hg_env,
                                     extra_ignore_errors=(1,))

        for line in raw_outgoing.splitlines():
            if not line:
                continue

            # Ignore warning messages that hg might put in, such as
            # "warning: certificate for foo can't be verified (Python too old)"
            if line.startswith('warning: '):
                continue

            try:
                rev, node, branch = (f.strip() for f in line.split('\t'))
            except Exception:
                raise Exception('Unexpected output from hg: %s' % line)

            branch = branch or 'default'
            assert rev is not None

            if not rev.isdigit():
                raise Exception('Unexpected output from hg: %s' % line)

            logging.debug('Found outgoing changeset %s:%s', rev, node)

            outgoing_changesets.append((int(rev), node, branch))

        return outgoing_changesets

    def _get_top_and_bottom_outgoing_revs(
        self,
        outgoing_changesets: list[tuple[int, str, str]],
    ) -> tuple[int, int]:
        """Return top and bottom outgoing revisions for the given changesets.

        Args:
            outgoing_changesets (list):
                A list of outgoing changesets.

        Returns:
            tuple:
            A 2-tuple containing the top and bottom revisions for the given
            outgoing changesets.
        """
        revs = {t[0] for t in outgoing_changesets}

        top_rev = max(revs)
        bottom_rev = min(revs)

        for rev, node, branch in reversed(outgoing_changesets):
            parents = self._execute(
                [self._exe, 'log', '-r', str(rev), '--template', '{parents}'],
                env=self._hg_env)
            parents = re.split(r':[^\s]+\s*', parents)
            parents = [int(p) for p in parents if p != '']

            parents = [p for p in parents if p not in outgoing_changesets]

            if len(parents) > 0:
                bottom_rev = parents[0]
                break
            else:
                bottom_rev = rev - 1

        bottom_rev = max(0, bottom_rev)

        return top_rev, bottom_rev

    def scan_for_server(
        self,
        repository_info: RepositoryInfo,
    ) -> Optional[str]:
        """Find the Review Board server matching this repository.

        Args:
            repository_info (rbtools.clients.base.repository.RepositoryInfo):
                The repository information structure.

        Returns:
            str:
            The Review Board server URL, if available.
        """
        server_url = self.hgrc.get('reviewboard.url', '').strip()

        if server_url:
            return server_url
        elif self._type == 'svn':
            # Try using the reviewboard:url property on the SVN repo, if it
            # exists.
            return SVNClient().scan_for_server(repository_info)

        return None

    def _execute(
        self,
        cmd: list[str],
        with_errors: bool = False,
        *args,
        **kwargs,
    ) -> Any:
        """Execute an hg command.

        Args:
            cmd (list of str):
                A command line to execute.

            with_errors (bool, optional):
                Whether to combine the output and error streams of the command
                together into a single return value.

                Unlike in :py:`rbtools.utils.process.execute`, this defaults
                to ``False``.

            *args (list):
                Additional arguments to pass to
                :py:func:`rbtools.utils.process.execute`.

            **kwargs (dict):
                Additional keyword arguments to pass to
                :py:func:`rbtools.utils.process.execute`.

        Returns:
            tuple:
            The result of the execute call.
        """
        # Don't modify the original arguments passed in. This interferes
        # with testing and could mess up callers.
        cmd = list(cmd)

        if '--hidden' in cmd and not self.hidden_changesets_supported:
            cmd.remove('--hidden')

        # Add our extension which normalizes settings. This is the easiest
        # way to normalize settings since it doesn't require us to chase
        # a tail of diff-related config options.
        cmd += [
            '--config',
            f'extensions.rbtoolsnormalize={self._hgext_path}',
        ]

        return execute(cmd, with_errors=with_errors, *args, **kwargs)

    def has_pending_changes(self) -> bool:
        """Check if there are changes waiting to be committed.

        Returns:
            bool:
            ``True`` if the working directory has been modified, otherwise
            returns ``False``.
        """
        status = self._execute([self._exe, 'status', '--modified', '--added',
                                '--removed', '--deleted'])
        return status != ''

    def supports_empty_files(self) -> bool:
        """Return whether the RB server supports added/deleted empty files.

        Returns:
            bool:
            ``True`` if the Review Board server supports showing empty files.
        """
        return (self.capabilities is not None and
                self.capabilities.has_capability('scmtools', 'mercurial',
                                                 'empty_files'))

    def get_current_bookmark(self) -> str:
        """Return the name of the current bookmark.

        Returns:
            str:
            A string with the name of the current bookmark.
        """
        return self._execute([self._exe, 'id', '-B'],
                             ignore_errors=True).strip()

    def get_file_content(
        self,
        *,
        filename: str,
        revision: str,
    ) -> bytes:
        """Return the contents of a file at a given revision.

        Version Added:
            5.0

        Args:
            filename (str):
                The file to fetch.

            revision (str):
                The revision of the file to get.

        Returns:
            bytes:
            The read file.
        """
        try:
            return self._execute(
                [self._exe, 'cat', '-r', revision, filename],
                env=self._hg_env,
                log_output_on_error=False,
                results_unicode=False)
        except Exception as e:
            raise SCMError(e)

    def get_file_size(
        self,
        *,
        filename: str,
        revision: str,
    ) -> int:
        """Return the size of a file at a given revision.

        Version Added:
            5.0

        Args:
            filename (str):
                The file to check.

            revision (str):
                The revision of the file to check.

        Returns:
            int:
            The size of the file, in bytes.
        """
        try:
            result = self._execute(
                [self._exe, 'files', '--template', '{size}', '-r', revision,
                 filename],
                env=self._hg_env,
                log_output_on_error=False)

            return int(result)
        except Exception as e:
            raise SCMError(e)
