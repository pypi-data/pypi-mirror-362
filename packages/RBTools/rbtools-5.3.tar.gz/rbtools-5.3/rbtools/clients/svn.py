"""A client for Subversion."""

from __future__ import annotations

import argparse
import io
import logging
import os
import posixpath
import re
import sys
from xml.etree import ElementTree
from typing import Dict, Iterator, List, Optional, TYPE_CHECKING, Tuple, cast
from urllib.parse import unquote

from rbtools.api.errors import APIError
from rbtools.api.resource import ListResource
from rbtools.clients import RepositoryInfo
from rbtools.clients.base.scmclient import (BaseSCMClient,
                                            SCMClientDiffResult,
                                            SCMClientPatcher,
                                            SCMClientRevisionSpec)
from rbtools.clients.errors import (AuthenticationError,
                                    InvalidRevisionSpecError,
                                    MinimumVersionError,
                                    OptionsCheckError,
                                    SCMClientDependencyError,
                                    SCMError,
                                    TooManyRevisionsError)
from rbtools.diffs.patches import PatchResult
from rbtools.diffs.writers import UnifiedDiffWriter
from rbtools.utils.checks import check_install
from rbtools.utils.console import get_pass
from rbtools.utils.diffs import (filename_match_any_patterns, filter_diff,
                                 normalize_patterns)
from rbtools.utils.filesystem import (make_empty_files, make_tempfile,
                                      walk_parents)
from rbtools.utils.process import (RunProcessError,
                                   RunProcessResult,
                                   run_process)
from rbtools.utils.streams import BufferedIterator

if TYPE_CHECKING:
    from rbtools.diffs.patches import Patch


logger = logging.getLogger(__name__)

_fs_encoding = sys.getfilesystemencoding()


class SVNPatcher(SCMClientPatcher['SVNClient']):
    """A patcher that applies Subversion patches to a tree.

    This applies patches using :command:`svn patch` and to manually handle
    added and deleted empty files.

    The patcher supports tracking conflicts and partially-applied patches.

    Version Added:
        5.1
    """

    ADDED_FILES_RE = re.compile(br'^Index:\s+(\S+)\t\(added\)$', re.M)
    DELETED_FILES_RE = re.compile(br'^Index:\s+(\S+)\t\(deleted\)$', re.M)

    SVN_PATCH_STATUS_RE = re.compile(
        br'^(?P<status>[ACDGU]) {9}(?P<filename>.+)$'
    )

    def get_default_prefix_level(
        self,
        *,
        patch: Patch,
        base_dir: Optional[str] = None,
    ) -> Optional[int]:
        """Return the default path prefix strip level for a patch.

        This function determines how much of a path to strip by default,
        if an explicit value isn't given.

        For Subversion, we always strip off any leading ``/``.

        Version Changed:
            5.0.2:
            * Added the ``base_dir`` argument and changed to prefer that
              if present.

        Args:
            patch (rbtools.diffs.patches.Patch):
                The path to generate a default prefix strip level for.

            base_dir (str, optional):
                The base directory to use when computing the prefix level,
                if available.

                Version Added:
                    5.0.2

        Returns:
            int:
            The prefix strip level, or ``None`` if a clear one could not be
            determined.
        """
        if (not base_dir and
            (repository_info := self.repository_info) is not None):
            base_dir = repository_info.base_path

        if base_dir == '/':
            # We always need to strip off the leading forward slash.
            return 1
        elif base_dir:
            # We strip all leading directories from base_dir. The last
            # directory will not be suffixed with a slash.
            return base_dir.count('/') + 1
        else:
            return None

    def apply_single_patch(
        self,
        *,
        patch: Patch,
        patch_num: int,
    ) -> PatchResult:
        """Apply a single patch.

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
        scmclient = self.scmclient

        # Make sure this is a version that supports patching. It should be
        # safe to assume a reasonable version these days, but this remains a
        # good bit of history and there's no harm.
        if scmclient.subversion_client_version < scmclient.PATCH_MIN_VERSION:
            raise MinimumVersionError(
                'Using "rbt patch" with the SVN backend requires at least '
                'svn 1.7.0')

        revert = self.revert
        repository_info = self.repository_info

        if repository_info is not None:
            checkout_base_dir = repository_info.base_path or ''
        else:
            checkout_base_dir = ''

        patch_file = str(patch.path)
        patch_base_dir = patch.base_dir

        in_subdir = (patch_base_dir and
                     checkout_base_dir != patch_base_dir and
                     checkout_base_dir.startswith(patch_base_dir))

        prefix_level = patch.prefix_level

        if prefix_level is None:
            # If we're in a subdirectory of where the patch was created, we
            # want to use the checkout directory to compute the prefix level.
            # If there's no overlap (or if the checkout and patch base
            # directories match), we use the patch basedir to compute the
            # prefix level and we hope that things apply cleanly.
            if in_subdir:
                base_dir = checkout_base_dir
            else:
                base_dir = patch_base_dir

            prefix_level = self.get_default_prefix_level(
                patch=patch, base_dir=base_dir)

            # Set this back so we can refer to it later when handling empty
            # files.
            patch.prefix_level = prefix_level

        if in_subdir:
            # The patch was created in a higher-level directory. Log a warning
            # and filter out any files which are not present in the current
            # directory.
            excluded, empty = self._exclude_files_not_in_tree(
                patch_file, checkout_base_dir)

            if excluded:
                logger.warning(
                    'This patch was generated in a different '
                    'directory. To prevent conflicts, all files '
                    'not under the current directory have been '
                    'excluded. To apply all files in this '
                    'patch, apply this patch from the %s directory.',
                    patch_base_dir)

                if empty:
                    logger.warning('All files were excluded from the patch.')

        # Build the command line.
        cmd: list[str] = ['patch']

        if prefix_level is not None and prefix_level >= 0:
            cmd.append(f'--strip={prefix_level}')

        if revert:
            cmd.append('--reverse-diff')

        cmd.append(patch_file)

        # Apply the patch.
        patch_output = (
            scmclient._run_svn(cmd,
                               ignore_errors=True,
                               redirect_stderr=True)
            .stdout_bytes
            .read()
        )

        # We'll now check the results of the application, and determine if
        # we need to handle empty files.
        #
        # We can't trust exit codes for svn patch, since we'll get 0 even if
        # we fail to patch anything. Instead, we'll look for the status output.
        applied: bool = False

        if self.can_patch_empty_files:
            applied = self.apply_patch_for_empty_files(patch)

        # Check for conflicts.
        patch_status_re = self.SVN_PATCH_STATUS_RE
        conflicting_files: list[str] = []

        for line in patch_output.splitlines():
            m = patch_status_re.match(line)

            if m:
                status = m.group('status')

                if status == b'C':
                    # There was a conflict.
                    conflicting_files.append(
                        m.group('filename').decode('utf-8'))
                else:
                    # Anything else is a successful result.
                    applied = True

        return PatchResult(applied=applied,
                           patch=patch,
                           patch_output=patch_output,
                           patch_range=(patch_num, patch_num),
                           has_conflicts=len(conflicting_files) > 0,
                           conflicting_files=conflicting_files)

    def apply_patch_for_empty_files(
        self,
        patch: Patch,
    ) -> bool:
        """Attempt to add or delete empty files in the patch.

        Args:
            patch (rbtools.diffs.patches.Patch):
                The opened patch to check and possibly apply.

        Returns:
            ``True`` if there are empty files in the patch that were applied.
            ``False`` if there were no empty files or the files could not be
            applied (which will lead to an error).
        """
        patched_empty_files: bool = False
        patch_content = patch.content
        prefix_level = patch.prefix_level
        scmclient = self.scmclient

        if self.revert:
            added_files_re = self.DELETED_FILES_RE
            deleted_files_re = self.ADDED_FILES_RE
        else:
            added_files_re = self.ADDED_FILES_RE
            deleted_files_re = self.DELETED_FILES_RE

        added_files = [
            _filename.decode('utf-8')
            for _filename in added_files_re.findall(patch_content)
        ]
        deleted_files = [
            _filename.decode('utf-8')
            for _filename in deleted_files_re.findall(patch_content)
        ]

        if added_files:
            if prefix_level:
                added_files = scmclient._strip_p_num_slashes(added_files,
                                                             prefix_level)

            make_empty_files(added_files)

            # We require --force here because svn will complain if we run
            # `svn add` on a file that has already been added or deleted.
            try:
                scmclient._run_svn(['add', '--force'] + added_files)
                patched_empty_files = True
            except RunProcessError:
                logger.error('Unable to execute "svn add" on: %s',
                             ', '.join(added_files))

        if deleted_files:
            if prefix_level:
                deleted_files = scmclient._strip_p_num_slashes(deleted_files,
                                                               prefix_level)

            # We require --force here because svn will complain if we run
            # `svn delete` on a file that has already been added or deleted.
            try:
                scmclient._run_svn(['delete', '--force'] + deleted_files)
                patched_empty_files = True
            except RunProcessError:
                logger.error('Unable to execute "svn delete" on: %s',
                             ', '.join(deleted_files))

        return patched_empty_files

    def _exclude_files_not_in_tree(
        self,
        patch_file: str,
        base_path: str,
    ) -> tuple[bool, bool]:
        """Process a diff and remove entries not in the current directory.

        Args:
            patch_file (str):
                The filename of the patch file to process. This file will be
                overwritten by the processed patch.

            base_path (str):
                The relative path between the root of the repository and the
                directory that the patch was created in.

        Returns:
            tuple:
            A 2-tuple of:

            Tuple:
                0 (bool):
                    Whether any files have been excluded.

                1 (bool):
                    Whether the diff is empty.
        """
        excluded_files = False
        empty_patch = True

        # If our base path does not have a trailing slash (which it won't
        # unless we are at a checkout root), we append a slash so that we can
        # determine if files are under the base_path. We do this so that files
        # like /trunkish (which begins with /trunk) do not mistakenly get
        # placed in /trunk if that is the base_path.
        if not base_path.endswith('/'):
            base_path += '/'

        filtered_patch_name = make_tempfile()

        with open(filtered_patch_name, 'wb') as filtered_patch, \
             open(patch_file, 'rb') as original_patch:
            include_file = True

            INDEX_FILE_RE = SVNClient.INDEX_FILE_RE

            for line in original_patch.readlines():
                m = INDEX_FILE_RE.match(line)

                if m:
                    filename = m.group(1).decode('utf-8')
                    include_file = filename.startswith(base_path)

                    if not include_file:
                        excluded_files = True
                    else:
                        empty_patch = False

                if include_file:
                    filtered_patch.write(line)

        os.rename(filtered_patch_name, patch_file)

        return excluded_files, empty_patch


class SVNClient(BaseSCMClient):
    """A client for Subversion.

    This is a wrapper around the svn executable that fetches repository
    information and generates compatible diffs.
    """

    scmclient_id = 'svn'
    name = 'Subversion'
    server_tool_names = 'Subversion'
    server_tool_ids = ['subversion']

    patcher_cls = SVNPatcher

    requires_diff_tool = True

    supports_diff_exclude_patterns = True
    supports_patch_revert = True

    can_get_file_content = True

    INDEX_SEP = b'=' * 67
    INDEX_FILE_RE = re.compile(br'^Index: (.+?)(?:\t\((added|deleted)\))?\n$')

    # Match the diff control lines generated by 'svn diff'.
    DIFF_ORIG_FILE_LINE_RE = re.compile(br'^---\s+.*\s+\(.*\)')
    DIFF_NEW_FILE_LINE_RE = re.compile(br'^\+\+\+\s+.*\s+\(.*\)')
    DIFF_COMPLETE_REMOVAL_RE = re.compile(br'^@@ -1,\d+ \+0,0 @@$')

    REVISION_WORKING_COPY = '--rbtools-working-copy'
    REVISION_CHANGELIST_PREFIX = '--rbtools-changelist:'

    VERSION_NUMBER_RE = re.compile(r'(\d+)\.(\d+)\.(\d+)')
    SHOW_COPIES_AS_ADDS_MIN_VERSION = (1, 7, 0)
    PATCH_MIN_VERSION = (1, 7, 0)

    ######################
    # Instance variables #
    ######################

    subversion_client_version: Tuple[int, int, int]

    def __init__(self, **kwargs) -> None:
        """Initialize the client.

        Args:
            **kwargs (dict):
                Keyword arguments to pass through to the superclass.
        """
        super(SVNClient, self).__init__(**kwargs)

        self._svn_info_cache: Dict[str, Optional[Dict[str, str]]] = {}
        self._svn_repository_info_cache: Optional[SVNRepositoryInfo] = None

    def check_dependencies(self) -> None:
        """Check whether all dependencies for the client are available.

        This checks for the presence of :command:`svn` in the system path.

        Version Added:
            4.0

        Raises:
            rbtools.clients.errors.SCMClientDependencyError:
                A git tool could not be found.
        """
        if not check_install(['svn', 'help']):
            raise SCMClientDependencyError(missing_exes=['svn'])

    def is_remote_only(self) -> bool:
        """Return whether this repository is operating in remote-only mode.

        For SVN, if a user provides the repository URL on the command line or
        config file, RBTools can proceed without a checkout.

        Returns:
            bool:
            Whether this repository is operating in remote-only mode.
        """
        # NOTE: This can be removed once check_dependencies() is mandatory.
        if not self.has_dependencies(expect_checked=True):
            logging.debug('Unable to execute "svn help": skipping SVN')
            return False

        repository_url = getattr(self.options, 'repository_url', None)

        if repository_url:
            info = self.svn_info(path=repository_url, ignore_errors=True)
            return bool(info and 'Repository Root' in info)

        return False

    def get_local_path(self) -> Optional[str]:
        """Return the local path to the working tree.

        Returns:
            str:
            The filesystem path of the repository on the client system.
        """
        # NOTE: This can be removed once check_dependencies() is mandatory.
        if not self.has_dependencies(expect_checked=True):
            logging.debug('Unable to execute "svn help": skipping SVN')
            return None

        info = self.svn_info(path=None, ignore_errors=True)

        if info and 'Working Copy Root Path' in info:
            return info['Working Copy Root Path']

        return None

    def get_repository_info(self) -> Optional[RepositoryInfo]:
        """Return repository information for the current working tree.

        Returns:
            SVNRepositoryInfo:
            The repository info structure.
        """
        if self._svn_repository_info_cache:
            return self._svn_repository_info_cache

        # NOTE: This can be removed once check_dependencies() is mandatory.
        if not self.has_dependencies(expect_checked=True):
            logging.debug('Unable to execute "svn help": skipping SVN')
            return None

        repository_url = getattr(self.options, 'repository_url', None)
        info = self.svn_info(path=repository_url,
                             ignore_errors=True)

        if not info:
            return None

        try:
            path = info['Repository Root']
            base_path = info['URL'][len(path):] or '/'
            uuid = info['Repository UUID']
        except KeyError:
            return None

        local_path = info.get('Working Copy Root Path')

        # Grab version of SVN client and store as a tuple in the form:
        #
        #   (major_version, minor_version, micro_version)
        ver_string = (
            self._run_svn(['--version', '-q'], ignore_errors=True)
            .stdout
            .read()
        )

        m = self.VERSION_NUMBER_RE.match(ver_string)

        if m:
            self.subversion_client_version = (
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
            )
        else:
            logging.warn('Unable to parse SVN client version triple from '
                         '"%s". Assuming version 0.0.0.', ver_string.strip())
            self.subversion_client_version = (0, 0, 0)

        self._svn_repository_info_cache = SVNRepositoryInfo(
            path=path,
            base_path=base_path,
            local_path=local_path,
            uuid=uuid,
            tool=self)

        return self._svn_repository_info_cache

    def find_matching_server_repository(
        self,
        repositories: ListResource,
    ) -> Tuple[Optional[ItemResource], Optional[ItemResource]]:
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
        repository_url = getattr(self.options, 'repository_url', None)
        info = self.svn_info(path=repository_url,
                             ignore_errors=True)

        if info:
            uuid = info['Repository UUID']

            for repository in repositories.all_items:
                try:
                    server_info = repository.get_info()
                except APIError:
                    continue

                if server_info and uuid == server_info['uuid']:
                    return repository, server_info

        return None, None

    def parse_revision_spec(
        self,
        revisions: List[str] = [],
    ) -> SCMClientRevisionSpec:
        """Parse the given revision spec.

        These will be used to generate the diffs to upload to Review Board
        (or print). The diff for review will include the changes in (base,
        tip].

        If a single revision is passed in, this will return the parent of
        that revision for "base" and the passed-in revision for "tip".

        If zero revisions are passed in, this will return the most recently
        checked-out revision for 'base' and a special string indicating the
        working copy for "tip".

        The SVN SCMClient never fills in the 'parent_base' key. Users who
        are using other patch-stack tools who want to use parent diffs with
        SVN will have to generate their diffs by hand.

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
        n_revisions = len(revisions)

        if n_revisions == 1 and ':' in revisions[0]:
            revisions = revisions[0].split(':')
            n_revisions = len(revisions)

        if n_revisions == 0:
            # Most recent checked-out revision -- working copy

            # TODO: this should warn about mixed-revision working copies that
            # affect the list of files changed (see bug 2392).
            return {
                'base': 'BASE',
                'tip': self.REVISION_WORKING_COPY,
            }
        elif n_revisions == 1:
            # Either a numeric revision (n-1:n) or a changelist
            revision_str = revisions[0]

            try:
                revision = self._convert_symbolic_revision(revision_str)
                return {
                    'base': revision - 1,
                    'tip': revision,
                }
            except ValueError:
                # It's not a revision--let's try a changelist. This only makes
                # sense if we have a working copy.
                if not self.options or not self.options.repository_url:
                    status = (
                        self._run_svn(
                            [
                                'status', '--cl', revision_str,
                                '--ignore-externals', '--xml',
                            ],
                            redirect_stderr=True)
                        .stdout_bytes
                        .read()
                    )
                    cl = ElementTree.fromstring(status).find('changelist')

                    if cl is not None:
                        # TODO: this should warn about mixed-revision working
                        # copies that affect the list of files changed (see
                        # bug 2392).
                        return {
                            'base': 'BASE',
                            'tip': (self.REVISION_CHANGELIST_PREFIX +
                                    revision_str),
                        }

                raise InvalidRevisionSpecError(
                    '"%s" does not appear to be a valid revision or '
                    'changelist name'
                    % revision_str)
        elif n_revisions == 2:
            # Diff between two numeric revisions
            try:
                return {
                    'base': self._convert_symbolic_revision(revisions[0]),
                    'tip': self._convert_symbolic_revision(revisions[1]),
                }
            except ValueError:
                raise InvalidRevisionSpecError(
                    'Could not parse specified revisions: %s' % revisions)
        else:
            raise TooManyRevisionsError

    def _convert_symbolic_revision(
        self,
        revision: str,
    ) -> int:
        """Convert a symbolic revision to a numbered revision.

        Args:
            revision (str):
                The name of a symbolic revision.

        Raises:
            ValueError:
                The given revision could not be converted.

        Returns:
            int:
            The revision number.
        """
        command: List[str] = ['-r', str(revision), '-l', '1']

        repository_url = getattr(self.options, 'repository_url', None)

        if repository_url:
            command.append(repository_url)

        log = self.svn_log_xml(command)

        if log is not None:
            try:
                root = ElementTree.fromstring(log)
            except ValueError as e:
                # _convert_symbolic_revision() nominally raises a ValueError to
                # indicate any failure to determine the revision number from
                # the log entry.  Here, we explicitly catch a ValueError from
                # ElementTree and raise a generic SCMError so that this
                # specific failure to parse the XML log output is
                # differentiated from the nominal case.
                raise SCMError('Failed to parse svn log - %s.' % e)

            logentry = root.find('logentry')
            if logentry is not None:
                return int(logentry.attrib['revision'])

        raise ValueError

    def scan_for_server(
        self,
        repository_info: RepositoryInfo,
    ) -> Optional[str]:
        """Scan for the reviewboard:url property in the repository.

        This method looks for the reviewboard:url property, which is an
        alternate (legacy) way of configuring the Review Board server URL
        inside a subversion repository.

        Args:
            repository_info (SVNRepositoryInfo):
                The repository information structure.

        Returns:
            str:
            The Review Board server URL, if available.
        """
        def get_url_prop(path):
            url = (
                self._run_svn(['propget', 'reviewboard:url', path],
                              ignore_errors=(1,))
                .stdout
                .read()
                .strip()
            )

            return url or None

        for path in walk_parents(os.getcwd()):
            if not os.path.exists(os.path.join(path, '.svn')):
                break

            prop = get_url_prop(path)
            if prop:
                return prop

        return get_url_prop(repository_info.path)

    def get_raw_commit_message(
        self,
        revisions: SCMClientRevisionSpec,
    ) -> str:
        """Return the raw commit message(s) for the given revisions.

        Args:
            revisions (dict):
                Revisions to get the commit messages for. This will contain
                ``tip`` and ``base`` keys.

        Returns:
            str:
            The commit messages for all the requested revisions.
        """
        base = str(revisions['base'])
        tip = str(revisions['tip'])

        if (tip == SVNClient.REVISION_WORKING_COPY or
            tip.startswith(SVNClient.REVISION_CHANGELIST_PREFIX)):
            return ''

        repository_url = getattr(self.options, 'repository_url', None)

        command: List[str] = ['-r', '%s:%s' % (base, tip)]

        if repository_url:
            command.append(repository_url)

        log = self.svn_log_xml(command) or b''

        try:
            root = ElementTree.fromstring(log)
        except ValueError as e:
            raise SCMError('Failed to parse svn log: %s' % e)

        # We skip the first commit message, because we want commit messages
        # corresponding to the changes that will be included in the diff.
        messages = root.findall('.//msg')[1:]

        return '\n\n'.join(
            message.text
            for message in messages
            if message.text is not None
        )

    def diff(
        self,
        revisions: SCMClientRevisionSpec,
        *,
        include_files: List[str] = [],
        exclude_patterns: List[str] = [],
        **kwargs,
    ) -> SCMClientDiffResult:
        """Perform a diff in a Subversion repository.

        If the given revision spec is empty, this will do a diff of the
        modified files in the working directory. If the spec is a changelist,
        it will do a diff of the modified files in that changelist. If the spec
        is a single revision, it will show the changes in that revision. If the
        spec is two revisions, this will do a diff between the two revisions.

        SVN repositories do not support branches of branches in a way that
        makes parent diffs possible, so we never return a parent diff.

        Args:
            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            include_files (list of str, optional):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of str, optional):
                A list of shell-style glob patterns to blacklist during diff
                generation.

            **kwargs (dict, unused):
                Unused keyword arguments.

        Returns:
            dict:
            A dictionary containing keys documented in
            :py:class:`rbtools.clients.base.scmclient.SCMClientDiffResult`.
        """
        repository_info = self.get_repository_info()
        assert repository_info is not None

        # SVN paths are always relative to the root of the repository, so we
        # compute the current path we are checked out at and use that as the
        # current working directory. We use / for the base_dir because we do
        # not normalize the paths to be filesystem paths, but instead use SVN
        # paths.
        exclude_patterns = normalize_patterns(
            patterns=exclude_patterns,
            base_dir='/',
            cwd=repository_info.base_path)

        # Keep track of information needed for handling empty files later.
        empty_files_revisions: SCMClientRevisionSpec = {
            'base': None,
            'tip': None,
        }

        base = str(revisions['base'])
        tip = str(revisions['tip'])

        diff_cmd: List[str] = ['diff', '--diff-cmd=diff', '--notice-ancestry']

        if (self.capabilities and
            self.capabilities.has_capability('diffs', 'file_attachments')):
            # Support for parsing the binary output when --force is included
            # was added along with support for binary files in diffs.
            diff_cmd.append('--force')

        changelist: Optional[str] = None

        if tip == self.REVISION_WORKING_COPY:
            # Posting the working copy
            diff_cmd += ['-r', base]
        elif tip.startswith(self.REVISION_CHANGELIST_PREFIX):
            # Posting a changelist
            changelist = tip[len(self.REVISION_CHANGELIST_PREFIX):]
            diff_cmd += ['--changelist', changelist]
        else:
            # Diff between two separate revisions. Behavior depends on whether
            # or not there's a working copy
            repository_url = getattr(self.options, 'repository_url', None)

            if repository_url:
                assert isinstance(repository_info.path, str)
                assert repository_info.base_path

                # No working copy--create 'old' and 'new' URLs
                if len(include_files) == 1:
                    # If there's a single file or directory passed in, we use
                    # that as part of the URL instead of as a separate
                    # filename.
                    repository_info.set_base_path(include_files[0])
                    include_files = []

                new_url = (repository_info.path + repository_info.base_path +
                           '@' + tip)

                # When the source revision is '0', assume the user wants to
                # upload a diff containing all the files in 'base_path' as
                # new files. If the base path within the repository is added to
                # both the old and new URLs, `svn diff` will error out, since
                # the base_path didn't exist at revision 0. To avoid that
                # error, use the repository's root URL as the source for the
                # diff.
                if base == '0':
                    old_url = repository_info.path + '@' + base
                else:
                    old_url = (repository_info.path +
                               repository_info.base_path + '@' + base)

                diff_cmd += [old_url, new_url]

                empty_files_revisions['base'] = '(revision %s)' % base
                empty_files_revisions['tip'] = '(revision %s)' % tip
            else:
                # Working copy--do a normal range diff
                diff_cmd.extend(['-r', '%s:%s' % (base, tip)])

                empty_files_revisions['base'] = '(revision %s)' % base
                empty_files_revisions['tip'] = '(revision %s)' % tip

        diff_cmd += include_files

        # Check for and validate --svn-show-copies-as-adds option, or evaluate
        # working copy to determine if scheduled commit will contain
        # addition-with-history commit. When this case occurs then
        # --svn-show-copies-as-adds must be specified. Note: this only
        # pertains to local modifications in a working copy and not diffs
        # between specific numeric revisions.
        if ((tip == self.REVISION_WORKING_COPY or changelist) and
            (self.subversion_client_version >=
             self.SHOW_COPIES_AS_ADDS_MIN_VERSION)):
            svn_show_copies_as_adds = getattr(
                self.options, 'svn_show_copies_as_adds', None)

            if svn_show_copies_as_adds is None:
                history_scheduled_with_commit = \
                    self.history_scheduled_with_commit(
                        repository_info=repository_info,
                        changelist=changelist,
                        include_files=include_files,
                        exclude_patterns=exclude_patterns)

                if history_scheduled_with_commit:
                    sys.stderr.write(
                        'One or more files in your changeset has history '
                        'scheduled with commit. Please try again with '
                        '"--svn-show-copies-as-adds=y/n".\n')
                    sys.exit(1)
            else:
                if svn_show_copies_as_adds in 'Yy':
                    diff_cmd.append('--show-copies-as-adds')

        diff_lines: Iterator[bytes] = (
            self._run_svn(diff_cmd, log_debug_output_on_error=False)
            .stdout_bytes
        )
        diff_lines = self.handle_renames(diff_lines)

        if self.supports_empty_files():
            diff_lines = self._handle_empty_files(diff_lines,
                                                  diff_cmd,
                                                  empty_files_revisions)

        diff_lines = self.convert_to_absolute_paths(diff_lines,
                                                    repository_info)

        if exclude_patterns:
            diff_lines = filter_diff(diff=diff_lines,
                                     file_index_re=self.INDEX_FILE_RE,
                                     exclude_patterns=exclude_patterns)

        return {
            'diff': b''.join(diff_lines),
        }

    def history_scheduled_with_commit(
        self,
        repository_info: RepositoryInfo,
        changelist: Optional[str],
        include_files: List[str],
        exclude_patterns: List[str],
    ) -> bool:
        """Return whether any files have history scheduled.

        Args:
            changelist (str):
                The changelist name, if specified.

            include_files (list of str):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of str):
                A list of shell-style glob patterns to blacklist during diff
                generation.

        Returns:
            bool:
            ``True`` if any new files have been scheduled including their
            history.
        """
        base_path = repository_info.base_path
        assert base_path

        status_cmd: List[str] = ['status', '-q', '--ignore-externals']

        if changelist:
            status_cmd += ['--changelist', changelist]

        if include_files:
            status_cmd += include_files

        for p in self._run_svn(status_cmd).stdout_bytes:
            try:
                if p[3:4] == b'+':
                    # We found a file with history, but first we must make
                    # sure that it is not being excluded.
                    should_exclude = (
                        bool(exclude_patterns) and
                        filename_match_any_patterns(
                            filename=p[8:].rstrip().decode(_fs_encoding),
                            patterns=exclude_patterns,
                            base_dir=base_path)
                    )

                    if not should_exclude:
                        return True
            except IndexError:
                # This may be some other output, or just doesn't have the
                # data we're looking for. Move along.
                pass

        return False

    def find_copyfrom(
        self,
        path: str,
    ) -> Optional[str]:
        """Find the source filename for copied files.

        The output of 'svn info' reports the "Copied From" header when invoked
        on the exact path that was copied. If the current file was copied as a
        part of a parent or any further ancestor directory, 'svn info' will not
        report the origin. Thus it is needed to ascend from the path until
        either a copied path is found or there are no more path components to
        try.

        Args:
            path (str):
                The filename of the copied file.

        Returns:
            str:
            The filename of the source of the copy.
        """
        def smart_join(
            p1: str,
            p2: Optional[str],
        ) -> str:
            if p2:
                return os.path.join(p1, p2)
            else:
                return p1

        path1: Optional[str] = path
        path2: Optional[str] = None

        while path1:
            info = self.svn_info(path1, ignore_errors=True) or {}
            url = info.get('Copied From URL', None)

            if url:
                root = info['Repository Root']
                from_path1 = unquote(url[len(root):])
                return smart_join(from_path1, path2)

            if info.get('Schedule', None) != 'normal':
                # Not added as a part of the parent directory, bail out
                return None

            # Strip one component from path1 to path2
            path1, tmp = os.path.split(path1)

            if path1 == '' or path1 == '/':
                path1 = None
            else:
                path2 = smart_join(tmp, path2)

        return None

    def handle_renames(
        self,
        diff_content: Iterator[bytes],
    ) -> Iterator[bytes]:
        """Fix up diff headers to properly show renames.

        The output of :command:`svn diff` is incorrect when the file in
        question came into being via svn mv/cp. Although the patch for these
        files are relative to its parent, the diff header doesn't reflect this.
        This function fixes the relevant section headers of the patch to
        portray this relationship.

        Args:
            diff_content (iterator of bytes):
                The lines of the diff to process.

        Yields:
            bytes:
            Each processed line of the diff.
        """
        # svn diff against a repository URL on two revisions appears to
        # handle moved files properly, so only adjust the diff file names
        # if they were created using a working copy.
        if getattr(self.options, 'repository_url', None):
            yield from diff_content
            return

        DIFF_COMPLETE_REMOVAL_RE = self.DIFF_COMPLETE_REMOVAL_RE
        DIFF_NEW_FILE_LINE_RE = self.DIFF_NEW_FILE_LINE_RE
        DIFF_ORIG_FILE_LINE_RE = self.DIFF_ORIG_FILE_LINE_RE
        INDEX_FILE_RE = self.INDEX_FILE_RE
        INDEX_SEP = self.INDEX_SEP

        iterator = BufferedIterator(diff_content)

        while not iterator.is_empty:
            lines = iterator.peek(4)

            if (len(lines) == 4 and
                INDEX_FILE_RE.match(lines[0]) and
                lines[1][:-1] == INDEX_SEP and
                DIFF_ORIG_FILE_LINE_RE.match(lines[2]) and
                DIFF_NEW_FILE_LINE_RE.match(lines[3])):
                # We found a diff header. Process it.
                lines = iterator.consume(5)

                # If the file is marked completely removed, bail out with the
                # original diff. The reason for this is that
                # ``svn diff --notice-ancestry`` generates two diffs for a
                # replaced file: one as a complete deletion, and one as a new
                # addition. If it was replaced with history, though, we need to
                # preserve the file name in the "deletion" part, or the patch
                # won't apply.
                if DIFF_COMPLETE_REMOVAL_RE.match(lines[4]):
                    yield from lines
                else:
                    from_line = lines[2]
                    to_line = lines[3]
                    to_file = self.parse_filename_header(to_line[4:])[0]
                    copied_from = self.find_copyfrom(to_file)

                    if copied_from is not None:
                        from_line = from_line.replace(
                            to_file.encode(_fs_encoding),
                            copied_from.encode(_fs_encoding))

                    yield lines[0]
                    yield lines[1]
                    yield from_line
                    yield to_line
                    yield lines[4]
            else:
                yield next(iterator)

    def _handle_empty_files(
        self,
        diff_content: Iterator[bytes],
        diff_cmd: List[str],
        revisions: SCMClientRevisionSpec,
    ) -> Iterator[bytes]:
        """Handle added and deleted 0-length files in the diff output.

        Since the diff output from :command:`svn diff` does not give enough
        context for 0-length files, we add extra information to the patch.

        For example, the original diff output of an added 0-length file is::

            Index: foo\\n
            ===================================================================\\n

        The modified diff of an added 0-length file will be::

            Index: foo\\t(added)\\n
            ===================================================================\\n
            --- foo\\t(<base_revision>)\\n
            +++ foo\\t(<tip_revision>)\\n

        Args:
            diff_content (iterator of bytes):
                The lines of the diff to process.

            diff_cmd (list of str):
                A partial command line to run :command:`svn diff`.

            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

        Yields:
            bytes:
            Each processed line of the diff.
        """
        # Get a list of all deleted files in this diff so we can differentiate
        # between added empty files and deleted empty files.
        try:
            diff_with_deleted = (
                self._run_svn(diff_cmd + ['--no-diff-deleted'])
                .stdout_bytes
                .read()
            )
        except RunProcessError:
            diff_with_deleted = None

        if not diff_with_deleted:
            yield from diff_content
            return

        deleted_files = re.findall(br'^Index:\s+(\S+)\s+\(deleted\)$',
                                   diff_with_deleted, re.M)

        iterator = BufferedIterator(diff_content)

        base: str
        tip: str

        while not iterator.is_empty:
            # Grab one more than we need, to detect if we're at the end.
            stream = io.BytesIO()
            diff_writer = UnifiedDiffWriter(stream)
            lines = iterator.peek(4)

            if (lines[0].startswith(b'Index: ') and
                (len(lines) < 4 or
                 (len(lines) == 4 and
                  lines[2].startswith(b'Index: ')))):
                index_tag: bytes

                # An empty file. Get and add the extra diff information.
                index_line = lines[0].strip()
                filename = index_line.split(b' ', 1)[1].strip()

                if filename in deleted_files:
                    # Deleted empty file.
                    index_tag = b'deleted'

                    if not revisions['base'] and not revisions['tip']:
                        tip = '(working copy)'
                        info = self.svn_info(filename.decode('utf-8'),
                                             ignore_errors=True)

                        if info and 'Revision' in info:
                            base = '(revision %s)' % info['Revision']
                        else:
                            next(iterator)
                            continue
                    else:
                        base = str(revisions['base'])
                        tip = str(revisions['tip'])
                else:
                    # Added empty file.
                    index_tag = b'added'

                    if not revisions['base'] and not revisions['tip']:
                        base = tip = '(revision 0)'
                    else:
                        base = str(revisions['base'])
                        tip = str(revisions['tip'])

                diff_writer.write_index(b'%s\t(%s)' % (filename, index_tag))
                diff_writer.write_file_headers(
                    orig_path=filename,
                    orig_extra=base,
                    modified_path=filename,
                    modified_extra=tip)

                # Skip the next line (the index separator) since we've already
                # copied it.
                iterator.consume(2)
            else:
                line = next(iterator)
                diff_writer.write_line(line.rstrip(b'\r\n'))

            # Yield the lines we just built.
            stream.seek(0)
            yield from stream

    def convert_to_absolute_paths(
        self,
        diff_content: Iterator[bytes],
        repository_info: RepositoryInfo,
    ) -> Iterator[bytes]:
        """Convert relative paths in a diff output to absolute paths.

        This handles paths that have been svn switched to other parts of the
        repository.

        Args:
            diff_content (iterator of bytes):
                The lines of the diff to process.

            repository_info (SVNRepositoryInfo):
                The repository info.

        Yields:
            bytes:
            Each processed line of the diff.
        """
        DIFF_NEW_FILE_LINE_RE = self.DIFF_NEW_FILE_LINE_RE
        DIFF_ORIG_FILE_LINE_RE = self.DIFF_ORIG_FILE_LINE_RE

        repository_url = getattr(self.options, 'repository_url', None)
        base_path = repository_info.base_path

        assert base_path

        for line in diff_content:
            front: Optional[bytes] = None
            orig_line: bytes = line

            if (DIFF_NEW_FILE_LINE_RE.match(line) or
                DIFF_ORIG_FILE_LINE_RE.match(line) or
                line.startswith(b'Index: ')):
                front, line = line.split(b' ', 1)

            if front:
                if line.startswith(b'/'):
                    # This is already absolute.
                    line = b'%s %s' % (front, line)
                else:
                    # Filename and rest of line (usually the revision
                    # component)
                    file, rest = self.parse_filename_header(line)

                    # If working with a diff generated outside of a working
                    # copy, then file paths are already absolute, so just
                    # add initial slash.
                    if repository_url:
                        path = unquote(posixpath.join(base_path, file))
                    else:
                        info = self.svn_info(file, ignore_errors=True)

                        if info is None:
                            yield orig_line
                            continue

                        url = info['URL']
                        root = info['Repository Root']
                        path = unquote(url[len(root):])

                    line = b'%s %s%s' % (front, path.encode(_fs_encoding),
                                         rest)

            yield line

    def svn_info(self, path, ignore_errors=False):
        """Return a dict which is the result of 'svn info' at a given path.

        Args:
            path (str):
                The path to the file being accessed.

            ignore_errors (bool, optional):
                Whether to ignore errors returned by ``svn info``.

        Returns:
            dict:
            The parsed ``svn info`` output.
        """
        # SVN's internal path recognizers think that any file path that
        # includes an '@' character will be path@rev, and skips everything that
        # comes after the '@'. This makes it hard to do operations on files
        # which include '@' in the name (such as image@2x.png).
        if path is not None and '@' in path and not path[-1] == '@':
            path += '@'

        if path not in self._svn_info_cache:
            cmdline: List[str] = ['info']

            if path is not None:
                cmdline.append(path)

            process_result = self._run_svn(cmdline,
                                           ignore_errors=ignore_errors)

            if process_result.exit_code == 0:
                svninfo: Dict[str, str] = {}

                for info in process_result.stdout:
                    parts = info.strip().split(': ', 1)

                    if len(parts) == 2:
                        key, value = parts
                        svninfo[key] = value

                self._svn_info_cache[path] = svninfo

            else:
                self._svn_info_cache[path] = None

        return self._svn_info_cache[path]

    def parse_filename_header(
        self,
        diff_line: bytes,
    ) -> Tuple[str, bytes]:
        """Parse the filename header from a diff.

        Args:
            diff_line (bytes):
                The line of the diff being parsed.

        Returns:
            tuple of (str, bytes):
            The parsed header line. The filename will be decoded using the
            system filesystem encoding.
        """
        parts: List[bytes] = []

        if b'\t' in diff_line:
            # There's a \t separating the filename and info. This is the
            # best case scenario, since it allows for filenames with spaces
            # without much work. The info can also contain tabs after the
            # initial one; ignore those when splitting the string.
            parts = diff_line.split(b'\t', 1)

        if b'  ' in diff_line:
            # There are spaces being used to separate the filename and info.
            # This is technically wrong, so all we can do is assume that
            # 1) the filename won't have multiple consecutive spaces, and
            # 2) there are at least 2 spaces separating the filename and info.
            parts = re.split(b'  +', diff_line, 1)

        if parts:
            return (parts[0].decode(_fs_encoding),
                    b'\t' + parts[1])

        # Strip off ending newline, and return it as the second component.
        return (diff_line.split(b'\n')[0].decode(_fs_encoding),
                b'\n')

    def supports_empty_files(self) -> bool:
        """Check if the server supports added/deleted empty files.

        Returns:
            bool:
            Whether the Review Board server supports empty added or deleted
            files.
        """
        return (self.capabilities is not None and
                self.capabilities.has_capability('scmtools', 'svn',
                                                 'empty_files'))

    def _run_svn(
        self,
        svn_args: List[str],
        **kwargs,
    ) -> RunProcessResult:
        """Run the ``svn`` command.

        Args:
            svn_args (list of str):
                A list of additional arguments to add to the SVN command line.

            **kwargs (dict):
                Additional keyword arguments to pass through to
                :py:func:`rbtools.utils.process.run_process`.

        Returns:
            rbtools.utils.process.RunProcessResult:
            The value returned by :py:func:`rbtools.utils.process.run_process`.
        """
        options = self.options or argparse.Namespace()
        svn_username = getattr(options, 'svn_username', None)
        svn_password = getattr(options, 'svn_password', None)
        svn_prompt_password = getattr(options, 'svn_prompt_password', False)

        cmdline: List[str] = ['svn', '--non-interactive'] + svn_args

        if svn_username:
            cmdline += ['--username', svn_username]

        if svn_prompt_password:
            # TODO: Remove this from here and move it somewhere less likely
            #       to cause problems.
            svn_password = get_pass('SVN Password: ')
            options.svn_prompt_password = False
            options.svn_password = svn_password

        if svn_password:
            cmdline += ['--password', svn_password]

        return run_process(cmdline, **kwargs)

    def svn_log_xml(
        self,
        svn_args: List[str],
        *args,
        **kwargs,
    ) -> Optional[bytes]:
        """Run SVN log non-interactively and retrieve XML output.

        We cannot run SVN log interactively and retrieve XML output because the
        authentication prompts will be intermixed with the XML output and cause
        XML parsing to fail.

        This function returns None (as if ``none_on_ignored_error`` were
        ``True``) if an error occurs that is not an authentication error.

        Args:
            svn_args (list of str):
                A list of additional arguments to add to the SVN command line.

            *args (list):
                Additional positional arguments to pass through to
                :py:func:`rbtools.utils.process.execute`.

            **kwargs (dict):
                Additional keyword arguments to pass through to
                :py:func:`rbtools.utils.process.execute`.

        Returns:
            bytes:
            The resulting log output.

        Raises:
            rbtools.clients.errors.AuthenticationError:
                Authentication to the remote repository failed.
        """
        try:
            return (
                self._run_svn(['log', '--xml'] + svn_args)
                .stdout_bytes
                .read()
            )
        except RunProcessError as e:
            errors = e.result.stderr_bytes.read()

            # SVN Error E215004: --non-interactive was passed but the remote
            # repository requires authentication.
            if errors.startswith(b'svn: E215004'):
                raise AuthenticationError(
                    'Could not authenticate against remote SVN repository. '
                    'Please provide the --svn-username and either the '
                    '--svn-password or --svn-prompt-password command line '
                    'options.')

            return None

    def check_options(self) -> None:
        """Verify the command line options.

        Raises:
            rbtools.clients.errors.OptionsCheckError:
                The supplied command line options were incorrect. In
                particular, if a file has history scheduled with the commit,
                the user needs to explicitly choose what behavior they want.
        """
        show_copies_as_adds = getattr(self.options, 'svn_show_copies_as_adds',
                                      None)

        if (show_copies_as_adds and
            (len(show_copies_as_adds) > 1 or
             show_copies_as_adds not in 'YyNn')):
            raise OptionsCheckError(
                'Invalid value \'%s\' for --svn-show-copies-as-adds '
                'option. Valid values are \'y\' or \'n\'.' %
                show_copies_as_adds)

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

        Raises:
            rbtools.clients.errors.SCMError:
                The file could not be found.
        """
        try:
            if revision == 'HEAD':
                with open(filename, 'rb') as f:
                    return f.read()
            else:
                return (
                    self._run_svn(['cat', '-r', revision, filename])
                    .stdout_bytes
                    .read()
                )
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

            revision (object):
                The revision of the file to check.

        Returns:
            int:
            The size of the file, in bytes.

        Raises:
            rbtools.client.errors.SCMError:
                An error occurred while attempting to get the file size.
        """
        try:
            if revision == 'HEAD':
                s = os.stat(filename)
                return s.st_size
            else:
                return int(
                    self._run_svn(['info', '--show-item', 'repos-size',
                                   '-r', revision, filename])
                    .stdout
                    .read()
                )
        except Exception as e:
            raise SCMError(e)


class SVNRepositoryInfo(RepositoryInfo):
    """Information on a Subversion repository.

    This stores information on the path and, optionally, UUID of a Subversion
    repository. It can match a local repository against those on a Review Board
    server.
    """

    ######################
    # Instance variables #
    ######################

    #: ID of the repository in the API.
    #:
    #: This is used primarily for testing purposes, and is not guaranteed to be
    #: set.
    #:
    #: Type:
    #:     int
    repository_id: Optional[int]

    #: UUID of the Subversion repository.
    #:
    #: Type:
    #:     str
    uuid: Optional[str]

    #: The SVN client that owns this repository information.
    #:
    #: Type:
    #:     SVNClient
    tool: Optional[SVNClient]

    def __init__(
        self,
        path: Optional[str] = None,
        base_path: Optional[str] = None,
        uuid: Optional[str] = None,
        local_path: Optional[str] = None,
        repository_id: Optional[int] = None,
        tool: Optional[SVNClient] = None,
    ) -> None:
        """Initialize the repository information.

        Args:
            path (str):
                Subversion checkout path.

            base_path (str):
                Root of the Subversion repository.

            local_path (str):
                The local filesystem path for the repository. This can
                sometimes be the same as ``path``, but may not be (since that
                can contain a remote repository path).

            uuid (str):
                UUID of the Subversion repository.

            repository_id (int, optional):
                ID of the repository in the API. This is used primarily for
                testing purposes, and is not guaranteed to be set.

            tool (rbtools.clients.base.scmclient.BaseSCMClient):
                The SCM client.
        """
        super(SVNRepositoryInfo, self).__init__(
            path=path,
            base_path=base_path,
            local_path=local_path)

        self.uuid = uuid
        self.repository_id = repository_id
        self.tool = tool

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
        url = cast(str, info['url'])
        root_url = cast(str, info['root_url'])

        repos_base_path = url[len(root_url):]
        relpath = self._get_relative_path(self.base_path, repos_base_path)

        if relpath:
            self.path = url
            self.base_path = relpath
            self.repository_id = cast(int, repository.id)

    def _get_relative_path(
        self,
        path: str,
        root: str,
    ) -> Optional[str]:
        pathdirs = self._split_on_slash(path)
        rootdirs = self._split_on_slash(root)

        # root is empty, so anything relative to that is itself
        if len(rootdirs) == 0:
            return path

        # If one of the directories doesn't match, then path is not relative
        # to root.
        if rootdirs != pathdirs[:len(rootdirs)]:
            return None

        # All the directories matched, so the relative path is whatever
        # directories are left over. The base_path can't be empty, though, so
        # if the paths are the same, return '/'
        if len(pathdirs) == len(rootdirs):
            return '/'
        else:
            return '/' + '/'.join(pathdirs[len(rootdirs):])

    def _split_on_slash(
        self,
        path: str,
    ) -> List[str]:
        # Split on slashes, but ignore multiple slashes and throw away any
        # trailing slashes.
        split = re.split('/+', path)

        if split[-1] == '':
            split = split[:-1]

        return split
