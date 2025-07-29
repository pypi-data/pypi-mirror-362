"""Base class for interfacing with source code management tools.

Version Added:
    4.0
"""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path
from typing import (Any, ClassVar, Dict, Generic, List, Mapping, Optional,
                    Sequence, TYPE_CHECKING, Tuple, TypeVar, Union, cast)

from typing_extensions import NotRequired, TypedDict, Unpack, final

from rbtools.clients.errors import (SCMClientDependencyError,
                                    SCMError)
from rbtools.deprecation import (RemovedInRBTools50Warning,
                                 RemovedInRBTools70Warning)
from rbtools.diffs.errors import ApplyPatchError
from rbtools.diffs.patcher import Patcher
from rbtools.diffs.patches import Patch
from rbtools.diffs.tools.registry import diff_tools_registry

if TYPE_CHECKING:
    from rbtools.api.capabilities import Capabilities
    from rbtools.api.resource import (ItemResource,
                                      ListResource,
                                      ReviewRequestResource)
    from rbtools.clients.base.repository import RepositoryInfo
    from rbtools.config import RBToolsConfig
    from rbtools.diffs.tools.base import BaseDiffTool
    from rbtools.diffs.patcher import PatcherKwargs
    from rbtools.diffs.patches import PatchAuthor, PatchResult


#: A generic type variable for BaseSCMClient subclasses.
#:
#: Version Added:
#:     5.1
TSCMClient = TypeVar('TSCMClient', bound='BaseSCMClient')


class SCMClientRevisionSpec(TypedDict):
    """A revision specification parsed from command line arguments.

    This class helps provide type hinting to results from
    :py:meth:`BaseSCMClient.parse_revision_spec`.

    The dictionary may include other arbitrary keys.

    Version Added:
        4.0
    """

    #: A revision to use as the base of the resulting diff.
    #:
    #: The value is considered an opaque value, dependent on the SCMClient.
    #:
    #: This is required.
    #:
    #: Type:
    #:     object
    base: Optional[object]

    #: A revision to use as the tip of the resulting diff.
    #:
    #: The value is considered an opaque value, dependent on the SCMClient.
    #:
    #: This is required.
    #:
    #: Type:
    #:     object
    tip: Optional[object]

    #: The revision to use as the base of a parent diff.
    #:
    #: The value is considered an opaque value, dependent on the SCMClient.
    #:
    #: This is optional.
    #:
    #: Type:
    #:     object
    parent_base: NotRequired[Optional[object]]

    #: The commit ID of the single commit being posted, if not using a range.
    #:
    #: This is optional.
    #:
    #: Type:
    #:     str
    commit_id: NotRequired[Optional[str]]

    #: Any extra revision state not used above.
    #:
    #: If a SCMClient needs to provide information in addition or instead of
    #: the above, they should populate this field, rather than placing the
    #: information in the main revision dictionary. This helps ensure a stable,
    #: typed interface for all revision data.
    #:
    #: Version Added:
    #:     4.0
    extra: NotRequired[Optional[Mapping[str, Any]]]


class SCMClientDiffResult(TypedDict):
    """The result of a diff operation.

    This class helps provide type hinting to results from
    :py:meth:`BaseSCMClient.diff`.

    Version Added:
        4.0
    """

    #: The contents of the diff to upload.
    #:
    #: This should be ``None`` or an empty string if diff generation fails.
    #:
    #: Type:
    #:     bytes
    diff: Optional[bytes]

    #: The contents of the parent diff, if available.
    #:
    #: Type:
    #:     bytes
    parent_diff: NotRequired[Optional[bytes]]

    #: The change number to include when posting, if available.
    #:
    #: Type:
    #:     str
    changenum: NotRequired[Optional[str]]

    #: The commit ID to include when posting, if available.
    #:
    #: Type:
    #:     str
    commit_id: NotRequired[Optional[str]]

    #: The ID of the commit that the change is based on, if available.
    #:
    #: This is necessary for some hosting services that don't provide
    #: individual file access.
    #:
    #: Type:
    #:     str
    base_commit_id: NotRequired[Optional[str]]

    #: A dictionary of extra_data keys to set on the review request.
    #:
    #: If posting a brand-new review request, these fields will be set on
    #: the review request itself.
    #:
    #: If updating an existing review request, these will be set on the draft.
    #
    #: This may contain structured data. It will be sent to the server
    #: as part of a JSON Merge Patch.
    #:
    #: This requires Review Board 3.0 or higher.
    #:
    #: Version Added:
    #:     3.1
    review_request_extra_data: NotRequired[Optional[Dict[str, Any]]]


class SCMClientCommitHistoryItem(TypedDict):
    """A commit in a commit history.

    This class helps provide type hinting to results from
    :py:meth:`BaseSCMClient.get_commit_history`.

    Version Added:
        4.0
    """

    #: The ID of the commit.
    #:
    #: Type:
    #:     str
    commit_id: str

    #: The ID of the parent commit.
    #:
    #: Type:
    #:     str
    parent_id: Optional[str]

    #: The commit message.
    #:
    #: Type:
    #:     str
    commit_message: Optional[str]

    #: The name of the commit's author.
    #:
    #: Type:
    #:     str
    author_name: Optional[str]

    #: The e-mail address of the commit's author.
    #:
    #: Type:
    #:     str
    author_email: Optional[str]

    #: The date the commit was authored.
    #:
    #: Type:
    #:     str
    author_date: Optional[str]

    #: The name of the person or entity who committed the change.
    #:
    #: Type:
    #:     str
    committer_name: NotRequired[Optional[str]]

    #: The e-mail address of the person or entity who committed the change.
    #:
    #: Type:
    #:     str
    committer_email: NotRequired[Optional[str]]

    #: The date the commit was made.
    #:
    #: Type:
    #:     str
    committer_date: NotRequired[Optional[str]]


class SCMClientCommitMessage(TypedDict):
    """A commit message from a local repository.

    This class helps provide type hinting to results from
    :py:meth:`BaseSCMClient.get_commit_message`.

    Version Added:
        4.0
    """

    #: The summary of a commit message.
    #:
    #: This should generally match the first line of a commit.
    #:
    #: Type:
    #:     str
    summary: Optional[str]

    #: The description of a commit message.
    #:
    #: This should generally match the remainder of the commit message after
    #: the summary, if any content remains.
    #:
    #: Type:
    #:     str
    description: NotRequired[Optional[str]]


class SCMClientPatcher(Generic[TSCMClient], Patcher):
    """A Patcher provided by a SCMClient.

    SCMClients that define custom patchers can subclass this to implement a
    new patcher. It takes care of storing initial state for the patcher based
    on the SCMClient, providing access to the parent SCMClient instance, and
    generating commits from patches.

    Version Added:
        5.1
    """

    ######################
    # Instance variables #
    ######################

    #: The SCMClient that owns the patcher.
    scmclient: TSCMClient

    def __init__(
        self,
        *,
        scmclient: TSCMClient,
        **kwargs: Unpack[PatcherKwargs],
    ) -> None:
        """Initialize the patcher.

        Args:
            scmclient (BaseSCMClient):
                The SCMClient object.
        """
        super().__init__(**kwargs)

        self.scmclient = scmclient
        self.can_patch_empty_files = scmclient.supports_empty_files()
        self.can_commit = (
            type(scmclient).create_commit is not
            BaseSCMClient.create_commit
        )

    def create_commit(
        self,
        *,
        patch_result: PatchResult,
        run_commit_editor: bool,
    ) -> None:
        """Internal method to create a commit based on a patch result.

        This will invoke the SCMClient's logic for committing files from
        a patch.

        Args:
            patch_result (rbtools.diffs.patches.PatchResult):
                The patch result containing the patch/patches to commit.

            run_commit_editor (bool):
                Whether to run the configured commit editor to alter the
                commit message.

        Raises:
            rbtools.diffs.errors.ApplyPatchResult:
                There was an error attempting to commit the patch.
        """
        patch = patch_result.patch
        assert patch

        author = patch.author
        message = patch.message

        assert author
        assert message

        self.scmclient.create_commit(author=author,
                                     message=message,
                                     run_editor=self.run_commit_editor)


class _LegacyPatcher(SCMClientPatcher['BaseSCMClient']):
    """A Patcher that wraps legacy SCMClient patching functions.

    This is used for SCMClients that don't yet support the modern patching
    support introduced in RBTools 5.1.

    This is scheduled to be removed in RBTools 7.

    Version Added:
        5.1
    """

    def apply_single_patch(
        self,
        *,
        patch: Patch,
        patch_num: int,
    ) -> PatchResult:
        """Internal function to apply a single patch.

        This will take a single patch and apply it using the SCMClient's
        legacy patching methods.

        Args:
            patch (rbtools.diffs.patches.Patch):
                The patch to apply, opened for reading.

            patch_num (int):
                The 1-based index of this patch in the full list of patches.

        Returns:
            rbtools.diffs.patches.PatchResult:
            The result of the patch application, whether the patch applied
            successfully or with normal patch failures.

        Raises:
            rbtools.diffs.errors.ApplyPatchResult:
                There was an error attempting to apply the patch.

                This won't be raised simply for conflicts or normal patch
                failures. It may be raised for errors encountered during
                the patching process.
        """
        repository_info = self.repository_info

        assert repository_info is not None

        # NOTE: Typing is bad here, but was before. It's non-trivial to sort
        #       out the base_path and base_dir typing requirements, since the
        #       logic and expectations are all over the map. We'll fix it with
        #       the move to the new Patcher support.
        base_path = repository_info.base_path
        base_dir = patch.base_dir or ''
        prefix_level = patch.prefix_level

        norm_prefix_level: Optional[str]

        if prefix_level is not None:
            norm_prefix_level = str(prefix_level)
        else:
            norm_prefix_level = None

        return self.scmclient.apply_patch(
            patch_file=str(patch.path),
            base_path=base_path,  # type: ignore
            base_dir=base_dir,
            p=norm_prefix_level,
            revert=self.revert)

    def apply_patch_for_empty_files(
        self,
        patch: Patch,
    ) -> bool:
        """Apply an empty file patch to a file.

        This will invoke the SCMClient's logic for applying a patch for an
        empty file.

        Args:
            patch (rbtools.diffs.patches.Patch):
                The opened patch to check and possibly apply.

        Returns:
            bool:
            ``True`` if there are empty files in the patch that were applied.
            ``False`` if there were no empty files or the files could not be
            applied (which will lead to an error).

        Raises:
            rbtools.diffs.errors.ApplyPatchError:
                There was an error while applying the patch.
        """
        norm_prefix_level: Optional[str]
        prefix_level = patch.prefix_level

        if prefix_level is not None:
            norm_prefix_level = str(prefix_level)
        else:
            norm_prefix_level = None

        return self.scmclient.apply_patch_for_empty_files(
            patch.content,
            p_num=norm_prefix_level,  # type: ignore
            revert=self.revert)


class BaseSCMClient:
    """A base class for interfacing with a source code management tool.

    These are used for fetching repository information and generating diffs.

    Callers must run :py:meth:`setup` or :py:meth:`has_dependencies` before
    calling methods on this tool.

    Version Changed:
        4.0:
        * Moved from :py:mod:`rbtools.clients` into
          :py:mod:`rbtools.clients.base.scmclient` and renamed from
          ``SCMClient`` to ``BaseSCMClient``.

        * A call to :py:meth:`setup` or :py:meth:`has_dependencies` will be
          required starting in RBTools 5.0.
    """

    #: The unique ID of the client.
    #:
    #: Version Added:
    #:     4.0:
    #:     This will be required in RBTools 5.0.
    #:
    #: Type:
    #:     str
    scmclient_id: str = ''

    #: The name of the client.
    #:
    #: Type:
    #:     str
    name: str = ''

    #: A comma-separated list of SCMClient names on the server.
    #:
    #: Version Added:
    #:    3.0
    #:
    #: Type:
    #:     str
    server_tool_names: ClassVar[Optional[str]] = None

    #: A comma-separated list of SCMClient IDs on the server.
    #:
    #: This supersedes :py:attr:`server_tool_names` when running on a version
    #: of Review Board that supports passing tool IDs to the repositories
    #: list API.
    #:
    #: Version Added:
    #:    5.0.1
    #:
    #: Type:
    #:     str
    server_tool_ids: ClassVar[Optional[List[str]]] = None

    #: Whether this tool requires a command line diff tool.
    #:
    #: This may be a boolean or a list.
    #:
    #: If a boolean, then this must be ``False`` if no command line tool is
    #: required, or ``True`` if any command line tool supported by RBTools is
    #: available (in which case the SCMClient is responsible for ensuring
    #: compatibility).
    #:
    #: If a list, then this must be a list of registered diff tool IDs that
    #: are compatible.
    #:
    #: Version Added:
    #:     4.0
    #:
    #: Type:
    #:     bool or list
    requires_diff_tool: Union[bool, List[str]] = False

    #: Whether the SCM uses server-side changesets
    #:
    #: Version Added:
    #:     3.0
    #:
    #: Type:
    #:     bool
    supports_changesets: bool = False

    #: Whether the SCM client can generate a commit history.
    #:
    #: Type:
    #:     bool
    supports_commit_history: bool = False

    #: Whether the SCM client's diff method takes the ``extra_args`` parameter.
    #:
    #: Type:
    #:     bool
    supports_diff_extra_args: bool = False

    #: Whether the SCM client supports excluding files from the diff.
    #:
    #: Type:
    #:     bool
    supports_diff_exclude_patterns: bool = False

    #: Whether the SCM client can generate diffs without renamed files.
    #:
    #: Type:
    #:     bool
    supports_no_renames: bool = False

    #: Whether the SCM client supports generating parent diffs.
    #:
    #: Version Added:
    #:     3.0
    #:
    #: Type:
    #:     bool
    supports_parent_diffs: bool = False

    #: Whether the SCM client supports reverting patches.
    #:
    #: Type:
    #:     bool
    supports_patch_revert: bool = False

    #: Whether commits can be amended.
    #:
    #: Type:
    #:     bool
    can_amend_commit: bool = False

    #: Whether the SCM can create merges.
    #:
    #: Type:
    #:     bool
    can_merge: bool = False

    #: Whether commits can be pushed upstream.
    #:
    #: Type:
    #:     bool
    can_push_upstream: bool = False

    #: Whether branch names can be deleted.
    #:
    #: Type:
    #:     bool
    can_delete_branch: bool = False

    #: Whether new branches can be created.
    #:
    #: Type:
    #:     bool
    can_branch: bool = False

    #: Whether new bookmarks can be created.
    #:
    #: Type:
    #:     bool
    can_bookmark: bool = False

    #: Whether commits can be squashed during merge.
    #:
    #: Type:
    #:     bool
    can_squash_merges: bool = False

    #: Whether the tool can get files at specific revisions.
    #:
    #: Version Added:
    #:     5.0
    #:
    #: Type:
    #:     bool
    can_get_file_content: bool = False

    #: The Patcher class used to apply patches.
    #:
    #: Version Added:
    #:     5.1:
    #:     This replaces the old :py:meth:`apply_patch` and
    #:     :py:meth:`apply_patch_for_empty_files` methods from earlier
    #:     releases.
    patcher_cls: type[SCMClientPatcher] = SCMClientPatcher

    ######################
    # Instance variables #
    ######################

    #: Capabilities returned by the server.
    #:
    #: This will be ``None`` if not set by the server.
    #:
    #: Type:
    #:     rbtools.api.capabilities.Capabilities
    capabilities: Optional[Capabilities]

    #: User configuration.
    #:
    #: Any user configuration loaded via :file:`.reviewboardrc` files.
    #: This may be empty.
    #:
    #: Type:
    #:     rbtools.config.config.RBToolsConfig
    config: RBToolsConfig

    #: Command line arguments passed to this client.
    #:
    #: This may be empty, and makes assumptions about which command line
    #: arguments are registered with a command. It's intended for use
    #: within RBTools.
    #:
    #: This may be ``None``.
    #:
    #: Type:
    #:     argparse.Namespace
    options: Optional[argparse.Namespace]

    #: Whether the client is set up and ready for operations.
    #:
    #: Operations may fail or crash if this is ``False``.
    #:
    #: Callers must call :py:meth:`setup` or :py:meth:`has_dependencies`
    #: before performing operations using this client.
    #:
    #: Version Added:
    #:     4.0
    #:
    #: Type:
    #:     bool
    is_setup: bool

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        options: Optional[argparse.Namespace] = None,
    ) -> None:
        """Initialize the client.

        Args:
            config (dict, optional):
                The loaded user config.

            options (argparse.Namespace, optional):
                The parsed command line arguments.
        """
        self.config = config or {}
        self.options = options
        self.capabilities = None
        self.is_setup = False

        self._diff_tool: Optional[BaseDiffTool] = None
        self._has_deps: Optional[bool] = None

    @final
    def setup(self) -> None:
        """Set up the client.

        This will perform checks to ensure the client can be used. Callers
        should make sure to either call this method or
        :py:meth:`has_dependencies` before performing any other operations
        on this client.

        If checks succeed, :py:attr:`is_setup` will be ``True``, and operations
        using this client can be performed.

        If checks fail, an exception may be raised, and :py:attr:`is_setup`
        will be ``False``.

        Note that this will not check :py:attr:`requires_diff_tool`, as that
        is only required for certain operations. Checking for a compatible
        diff tool is the responsibility of the caller whenever working with
        diffs.

        Version Added:
            4.0

        Raises:
            rbtools.clients.errors.SCMClientDependencyError:
                One or more required dependencies are missing.
        """
        if self.is_setup:
            # Silently return. We may want to make this a warning in a future
            # version, or enforce call order, but it's currently harmless to
            # allow multiple calls.
            return

        try:
            self.check_dependencies()
            self._has_deps = True
        except SCMClientDependencyError:
            self._has_deps = False
            raise

        self.is_setup = True

    def has_dependencies(
        self,
        expect_checked: bool = False,
    ) -> bool:
        """Return whether all dependencies for the client are available.

        Either this or :py:meth:`setup` must be called before any operations
        are performed with this client.

        Version Added:
            4.0

        Args:
            expect_checked (bool, optional):
                Whether the caller expects that dependency checking has
                already been done.

                If ``True``, and dependencies have not yet been checked via
                :py:meth:`check_dependencies`, this will raise a deprecation
                warning.

                Starting in RBTools 4.0, this will raise an exception if
                :py:meth:`check_dependencies` hasn't yet been called.

        Returns:
            bool:
            ``True`` if dependencies are all available. ``False`` if one or
            more are not.
        """
        if self._has_deps is None:
            if expect_checked:
                RemovedInRBTools50Warning.warn(
                    'Either %(cls_name)s.setup() or '
                    '%(cls_name)s.has_dependencies() must be called before '
                    'other functions are used. This will be required '
                    'starting in RBTools 5.0.'
                    % {
                        'cls_name': type(self).__name__,
                    })

            try:
                self.setup()
            except SCMClientDependencyError:
                pass

        return cast(bool, self._has_deps)

    def check_dependencies(self) -> None:
        """Check whether the base dependencies needed are available.

        This is responsible for checking for any command line tools or Python
        modules required to consider this client as an option when scanning
        repositories or selecting a specific client.

        This should not check for diff implementations or anything specific
        about a local filesystem. It's merely a first-pass dependency check.

        This function is normally called via :py:meth:`setup` (which will
        re-raise any exceptions here) or :py:meth:`has_dependencies`. It
        doesn't need to be called manually unless attempting to re-generate
        the exception.

        Subclasses can log any failed checks in the debug log, to help with
        debugging missing tools. If checking against multiple possible names,
        they may also record information needed to locate the matching
        executable for future operations.

        It's recommended to use :py:meth:`rbtools.utils.checks.check_install`
        to help with executable dependency checks.

        Version Added:
            4.0

        Raises:
            rbtools.clients.errors.SCMClientDependencyError:
                One or more required dependencies are missing.
        """
        pass

    def is_remote_only(self) -> bool:
        """Return whether this repository is operating in remote-only mode.

        For some SCMs and some operations, it may be possible to operate
        exclusively with a remote server and have no working directory.

        Version Added:
            3.0

        Returns:
            bool:
            Whether this repository is operating in remote-only mode.
        """
        return False

    def get_local_path(self) -> Optional[str]:
        """Return the local path to the working tree.

        This is expected to be overridden by subclasses.

        Version Added:
            3.0

        Returns:
            str:
            The filesystem path of the repository on the client system.
        """
        logging.warning('%s should implement a get_local_path method',
                        self.__class__)
        info = self.get_repository_info()

        if info:
            return info.local_path

        return None

    def get_repository_info(self) -> Optional[RepositoryInfo]:
        """Return repository information for the current working tree.

        This is expected to be overridden by subclasses.

        Version Added:
            3.0

        Returns:
            rbtools.clients.base.repository.RepositoryInfo:
            The repository info structure.
        """
        return None

    def get_diff_tool(self) -> Optional[BaseDiffTool]:
        """Return a diff tool for use with this client.

        This can be used by subclasses, and by callers that want to check if
        a compatible diff tool is available before calling :py:meth:`diff`.

        The value is cached for the client.

        Version Added:
            4.0

        Returns:
            rbtools.diffs.tools.base.BaseDiffTool:
            The diff instance, if a compatible instance is found.

            This will be ``None`` if :py:attr:`requires_diff_tool` is
            ``False``.

        Raises:
            TypeError:
                :py:attr:`requires_diff_tool` was an unsupported type.

            rbtools.diffs.tools.errors.MissingDiffToolError:
                No compatible diff tool could be found.
        """
        diff_tool = self._diff_tool

        if diff_tool is None:
            if self.requires_diff_tool is True:
                diff_tool = diff_tools_registry.get_available()
            elif self.requires_diff_tool is False:
                diff_tool = None
            elif isinstance(self.requires_diff_tool, list):
                diff_tool = diff_tools_registry.get_available(
                    compatible_diff_tool_ids=self.requires_diff_tool)
            else:
                raise TypeError(
                    'Unexpected type %s for %s.requires_diff_tool.'
                    % (type(self.requires_diff_tool), type(self).__name__))

            self._diff_tool = diff_tool

        return diff_tool

    def get_server_tool_names(
        self,
        capabilities: Optional[Capabilities],
    ) -> Optional[str]:
        """Return the list of supported tool names on the server.

        Version Added:
            5.0.1

        Args:
            capabilities (rbtools.api.capabilities.Capabilities):
                The server capabilities, if present.

        Returns:
            str:
            A comma-separated list of server-side tool names to match with.
        """
        if (capabilities is not None and
            capabilities.get_capability('scmtools', 'supported_tools') and
            self.server_tool_ids is not None):
            # Versions of Review Board that have this capability allow us to
            # pass SCMTool IDs rather than names.
            return ','.join(self.server_tool_ids)
        else:
            return self.server_tool_names

    def get_patcher(
        self,
        **kwargs: Unpack[PatcherKwargs],
    ) -> SCMClientPatcher:
        """Return a patcher for this client.

        Version Added:
            5.1

        Args:
            **kwargs (dict):
                Keyword arguments to pass to the patcher.

                See :py:class:`~rbtools.diffs.patcher.Patcher` for details.

        Returns:
            SCMClientPatcher:
            The patcher used to apply patches for this client.
        """
        patcher_cls = self.patcher_cls
        scmclient_cls = type(self)

        if (scmclient_cls.apply_patch is not BaseSCMClient.apply_patch and
            patcher_cls is BaseSCMClient.patcher_cls):
            # This is a legacy SCMClient implementation that overrode
            # apply_patch() without providing a custom patcher. We need to
            # return a compatibility wrapper.
            RemovedInRBTools70Warning.warn(
                '%(name)s must be updated to set a custom patcher class as '
                '%(name)s.patcher_cls. Support for apply_patch() will be '
                'removed in RBTools 7.'
                % {
                    'name': scmclient_cls.__name__,
                })
            patcher_cls = _LegacyPatcher

        return patcher_cls(scmclient=self, **kwargs)

    def find_matching_server_repository(
        self,
        repositories: ListResource,
    ) -> Tuple[Optional[ItemResource], Optional[ItemResource]]:
        """Find a match for the repository on the server.

        Version Added:
            3.0

        Args:
            repositories (rbtools.api.resource.ListResource):
                The fetched repositories.

        Returns:
            tuple:
            A 2-tuple of matching repository information:

            Tuple:
                0 (rbtools.api.resource.ItemResource):
                    The matching repository resource, if found.

                    If not found, this will be ``None``.

                1 (rbtools.api.resource.ItemResource):
                    The matching repository information resource, if found.

                    If not found, this will be ``None``.
        """
        return None, None

    def get_repository_name(self) -> Optional[str]:
        """Return any repository name configured in the repository.

        This is used as a fallback from the standard config options, for
        repository types that support configuring the name in repository
        metadata.

        Version Added:
            3.0

        Returns:
            str:
            The configured repository name, or None.
        """
        return None

    def check_options(self) -> None:
        """Verify the command line options.

        This is expected to be overridden by subclasses, if they need to do
        specific validation of the command line.

        Raises:
            rbtools.clients.errors.OptionsCheckError:
                The supplied command line options were incorrect. In
                particular, if a file has history scheduled with the commit,
                the user needs to explicitly choose what behavior they want.
        """
        pass

    def get_changenum(
        self,
        revisions: SCMClientRevisionSpec,
    ) -> Optional[str]:
        """Return the change number for the given revisions.

        This is only used when the client is supposed to send a change number
        to the server (such as with Perforce).

        Args:
            revisions (dict):
                A revisions dictionary as returned by
                :py:meth:`parse_revision_spec`.

        Returns:
            str:
            The change number to send to the Review Board server.
        """
        return None

    def scan_for_server(
        self,
        repository_info: RepositoryInfo,
    ) -> Optional[str]:
        """Find the server path.

        This will search for the server name in the .reviewboardrc config
        files. These are loaded with the current directory first, and searching
        through each parent directory, and finally $HOME/.reviewboardrc last.

        Args:
            repository_info (rbtools.clients.base.repository.RepositoryInfo):
                The repository information structure.

        Returns:
            str:
            The Review Board server URL, if available.
        """
        return None

    def parse_revision_spec(
        self,
        revisions: List[str] = [],
    ) -> SCMClientRevisionSpec:
        """Parse the given revision spec.

        The 'revisions' argument is a list of revisions as specified by the
        user. Items in the list do not necessarily represent a single revision,
        since the user can use SCM-native syntaxes such as "r1..r2" or "r1:r2".
        SCMTool-specific overrides of this method are expected to deal with
        such syntaxes.

        Args:
            revisions (list of str, optional):
                A list of revisions as specified by the user. Items in the list
                do not necessarily represent a single revision, since the user
                can use SCM-native syntaxes such as ``r1..r2`` or ``r1:r2``.
                SCMTool-specific overrides of this method are expected to deal
                with such syntaxes.

        Returns:
            dict:
            A dictionary containing keys found in
            :py:class:`SCMClientRevisionSpec`.

            Additional keys may be included by subclasses for their own
            internal use.

            These will be used to generate the diffs to upload to Review Board
            (or print). The diff for review will include the changes in (base,
            tip], and the parent diff (if necessary) will include (parent,
            base].

            If a single revision is passed in, this will return the parent of
            that revision for "base" and the passed-in revision for "tip".

            If zero revisions are passed in, this will return revisions
            relevant for the "current change". The exact definition of what
            "current" means is specific to each SCMTool backend, and documented
            in the implementation classes.

        Raises:
            rbtools.clients.errors.InvalidRevisionSpecError:
                The given revisions could not be parsed.

            rbtools.clients.errors.TooManyRevisionsError:
                The specified revisions list contained too many revisions.
        """
        return {
            'base': None,
            'tip': None,
        }

    def get_tree_matches_review_request(
        self,
        review_request: ReviewRequestResource,
        *,
        revisions: SCMClientRevisionSpec,
        **kwargs,
    ) -> Optional[bool]:
        """Return whether a review request matches revisions or tree state.

        This works along with review request matching in tools like
        :command:`rbt post` to match state in a review request (such as in
        ``extra_data``) with the state in the local tree (such as the local
        branch or SCM-specific identifiers other than a commit ID).

        Subclasses can override this to implement their own matching logic.
        By default, no additional logic is implemented.

        Version Added:
            3.1

        Args:
            review_request (rbtools.api.resource.ReviewRequestResource):
                The review request being matched.

            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            **kwargs (dict, unused):
                Additional keyword arguments, for future expansion.

        Returns:
            bool:
            ``True`` if the review request is considered an exact match.

            ``False`` if the review request should be explicitly discarded
            as a possible match.

            ``None`` if a match could not be determined based on available
            information.
        """
        return None

    def diff(
        self,
        revisions: SCMClientRevisionSpec,
        *,
        include_files: List[str] = [],
        exclude_patterns: List[str] = [],
        no_renames: bool = False,
        repository_info: Optional[RepositoryInfo] = None,
        extra_args: List[str] = [],
        with_parent_diff: bool = True,
    ) -> SCMClientDiffResult:
        """Perform a diff using the given revisions.

        Callers should make sure that the appropriate diff tool is installed
        by calling :py:func:`rbtools.diffs.tools.registry.get_diff_tool` and
        passing :py:attr:`requires_diff_tool` if it's a list.

        This is expected to be overridden by subclasses, which should:

        1. Set :py:attr:`requires_diff_tool` based on the client's needs.
        2. Optionally use :py:attr:`options` for any client-specific diff
           functionality.
        3. Call :py:meth:`get_diff_tool` early, if needed.

        Subclasses that need to support special arguments should use
        :py:attr:`options`.

        Version Changed:
            4.0:
            * All arguments except ``revisions`` must be specified as keyword
              arguments.
            * Subclasses should now use :py:attr:`requires_diff_tool` and
              :py:meth:`get_diff_tool` instead of manually invoking
              :command:`diff` tools.

        Args:
            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            include_files (list of str, optional):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of str, optional):
                A list of shell-style glob patterns to blacklist during diff
                generation.

            no_renames (bool, optional):
                Whether to avoid rename detection.

            repository_info (rbtools.clients.base.repository.RepositoryInfo,
                             optional):
                The repository info structure.

            extra_args (list, unused):
                Additional arguments to be passed to the diff generation.

            with_parent_diff (bool, optional):
                Whether or not to compute a parent diff.

        Returns:
            dict:
            A dictionary containing keys documented in
            :py:class:`SCMClientDiffResult`.
        """
        return {
            'diff': None,
            'parent_diff': None,
            'commit_id': None,
            'base_commit_id': None,
            'review_request_extra_data': None,
        }

    def get_commit_history(
        self,
        revisions: SCMClientRevisionSpec,
    ) -> Optional[List[SCMClientCommitHistoryItem]]:
        """Return the commit history between the given revisions.

        Derived classes must override this method if they support posting with
        history.

        Args:
            revisions (dict):
                The parsed revision spec to use to generate the history.

        Returns:
            list of dict:
            The history entries.
        """
        raise NotImplementedError

    def _get_p_number(
        self,
        base_path: str,
        base_dir: str,
    ) -> int:
        """Return the appropriate value for the -p argument to patch.

        This function returns an integer. If the integer is -1, then the -p
        option should not be provided to patch. Otherwise, the return value is
        the argument to :command:`patch -p`.

        Args:
            base_path (str):
                The relative path between the repository root and the
                directory that the diff file was generated in.

            base_dir (str):
                The current relative path between the repository root and the
                user's working directory.

        Returns:
            int:
            The prefix number to pass into the :command:`patch` command.
        """
        if base_path and base_dir.startswith(base_path):
            return base_path.count('/') + 1
        else:
            return -1

    def _strip_p_num_slashes(
        self,
        files: List[str],
        p_num: int,
    ) -> List[str]:
        """Strip the smallest prefix containing p_num slashes from filenames.

        To match the behavior of the :command:`patch -pX` option, adjacent
        slashes are counted as a single slash.

        Args:
            files (list of str):
                The filenames to process.

            p_num (int):
                The number of prefixes to strip.

        Returns:
            list of str:
            The processed list of filenames.
        """
        if p_num > 0:
            regex = re.compile(r'[^/]*/+')
            return [regex.sub('', f, p_num) for f in files]
        else:
            return files

    def has_pending_changes(self) -> bool:
        """Return whether there are changes waiting to be committed.

        Derived classes should override this method if they wish to support
        checking for pending changes.

        Returns:
            bool:
            ``True`` if the working directory has been modified or if changes
            have been staged in the index.
        """
        raise NotImplementedError

    def apply_patch(
        self,
        patch_file: str,
        *,
        base_path: str,
        base_dir: str,
        p: Optional[str] = None,
        revert: bool = False,
    ) -> PatchResult:
        """Apply the patch and return a PatchResult indicating its success.

        Args:
            patch_file (str):
                The name of the patch file to apply.

            base_path (str):
                The base path that the diff was generated in.

            base_dir (str):
                The path of the current working directory relative to the root
                of the repository.

            p (str, optional):
                The prefix level of the diff.

            revert (bool, optional):
                Whether the patch should be reverted rather than applied.

        Returns:
            rbtools.clients.base.patch.PatchResult:
            The result of the patch operation.
        """
        if p is None:
            p_num = None
        else:
            try:
                p_num = int(p)
            except ValueError:
                logging.warning('Invalid -p value: %s; assuming zero.', p)
                p_num = None

        repository_info = self.get_repository_info()

        patcher = self.get_patcher(
            patches=[
                Patch(path=Path(patch_file),
                      base_dir=base_dir,
                      prefix_level=p_num),
            ],
            revert=revert,
            repository_info=repository_info)

        results: Sequence[PatchResult]

        try:
            results = list(patcher.patch())
        except ApplyPatchError as e:
            if e.failed_patch_result:
                results = [e.failed_patch_result]
            else:
                raise SCMError(str(e))

        assert len(results) == 1
        return results[0]

    def create_commit(
        self,
        *,
        message: str,
        author: PatchAuthor,
        run_editor: bool,
        files: List[str] = [],
        all_files: bool = False,
    ) -> None:
        """Create a commit based on the provided message and author.

        Derived classes should override this method if they wish to support
        committing changes to their repositories.

        Args:
            message (str):
                The commit message to use.

            author (rbtools.clients.base.patch.PatchAuthor):
                The author of the commit.

            run_editor (bool):
                Whether to run the user's editor on the commit message before
                committing.

            files (list of str, optional):
                The list of filenames to commit.

            all_files (bool, optional):
                Whether to commit all changed files, ignoring the ``files``
                argument.

        Raises:
            NotImplementedError:
                The client does not support creating commits.

            rbtools.clients.errors.CreateCommitError:
                The commit message could not be created. It may have been
                aborted by the user.
        """
        raise NotImplementedError

    def get_commit_message(
        self,
        revisions: SCMClientRevisionSpec,
    ) -> Optional[SCMClientCommitMessage]:
        """Return the commit message from the commits in the given revisions.

        This pulls out the first line from the commit messages of the given
        revisions. That is then used as the summary.

        Args:
            revisions (dict):
                A dictionary as returned by :py:meth:`parse_revision_spec`.

        Returns:
            dict:
            A dictionary containing keys found in
            :py:class:`SCMClientCommitMessage`.

            This may be ``None``, if no commit message is found.
        """
        commit_message = self.get_raw_commit_message(revisions)
        lines = commit_message.splitlines()

        if not lines:
            return None

        result: SCMClientCommitMessage = {
            'summary': lines[0],
        }

        # Try to pull the body of the commit out of the full commit
        # description, so that we can skip the summary.
        if len(lines) >= 3 and lines[0] and not lines[1]:
            result['description'] = '\n'.join(lines[2:]).strip()
        else:
            result['description'] = commit_message

        return result

    def delete_branch(
        self,
        branch_name: str,
        *,
        merged_only: bool = True,
    ) -> None:
        """Delete the specified branch.

        Args:
            branch_name (str):
                The name of the branch to delete.

            merged_only (bool, optional):
                Whether to limit branch deletion to only those branches which
                have been merged into the current HEAD.

        Raises:
            rbtools.clients.errors.SCMError:
                An error occurred while deleting the branch.
        """
        raise NotImplementedError

    def merge(
        self,
        *,
        target: str,
        destination: str,
        message: str,
        author: PatchAuthor,
        squash: bool = False,
        run_editor: bool = False,
        close_branch: bool = True,
    ) -> None:
        """Merge the target branch with destination branch.

        Args:
            target (str):
                The name of the branch to merge.

            destination (str):
                The name of the branch to merge into.

            message (str):
                The commit message to use.

            author (rbtools.clients.base.patch.PatchAuthor):
                The author of the commit.

            squash (bool, optional):
                Whether to squash the commits or do a plain merge.

            run_editor (bool, optional):
                Whether to run the user's editor on the commit message before
                committing.

            close_branch (bool, optional):
                Whether to close/delete the merged branch.

        Raises:
            rbtools.clients.errors.MergeError:
                An error occurred while merging the branch.
        """
        raise NotImplementedError

    def push_upstream(
        self,
        remote_branch: str,
    ) -> None:
        """Push the current branch to upstream.

        Args:
            remote_branch (str):
                The name of the branch to push to.

        Raises:
            rbtools.client.errors.PushError:
                The branch was unable to be pushed.
        """
        raise NotImplementedError

    def get_raw_commit_message(
        self,
        revisions: SCMClientRevisionSpec,
    ) -> str:
        """Extract the commit messages on the commits in the given revisions.

        Derived classes should override this method in order to allow callers
        to fetch commit messages. This is needed for description guessing.

        If a derived class is unable to fetch the description, ``None`` should
        be returned.

        Callers that need to differentiate the summary from the description
        should instead use get_commit_message().

        Args:
            revisions (dict):
                A dictionary containing ``base`` and ``tip`` keys.

        Returns:
            str:
            The commit messages of all commits between (base, tip].
        """
        raise NotImplementedError

    def get_current_branch(self) -> str:
        """Return the repository branch name of the current directory.

        Derived classes should override this method if they are able to
        determine the current branch of the working directory.

        Returns:
            str:
            A string with the name of the current branch. If the branch is
            unable to be determined, returns ``None``.
        """
        raise NotImplementedError

    def supports_empty_files(self) -> bool:
        """Return whether the server supports added/deleted empty files.

        Returns:
            bool:
            ``True`` if the Review Board server supports added or deleted empty
            files.
        """
        return False

    def apply_patch_for_empty_files(
        self,
        patch: bytes,
        *,
        p_num: str,
        revert: bool = False,
    ) -> bool:
        """Return whether any empty files in the patch are applied.

        Args:
            patch (bytes):
                The contents of the patch.

            p_num (str):
                The prefix level of the diff.

            revert (bool, optional):
                Whether the patch should be reverted rather than applied.

        Returns:
            bool:
            ``True`` if there are empty files in the patch. ``False`` if there
            were no empty files, or if an error occurred while applying the
            patch.
        """
        raise NotImplementedError

    def amend_commit_description(
        self,
        message: str,
        *,
        revisions: Optional[SCMClientRevisionSpec] = None,
    ) -> None:
        """Update a commit message to the given string.

        Args:
            message (str):
                The commit message to use when amending the commit.

            revisions (dict, optional):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`. This provides compatibility
                with SCMs that allow modifications of multiple changesets at
                any given time, and will amend the change referenced by the
                ``tip`` key.

        Raises:
            rbtools.clients.errors.AmendError:
                The amend operation failed.
        """
        raise NotImplementedError

    def get_file_content(
        self,
        *,
        filename: str,
        revision: str,
    ) -> bytes:
        """Return the contents of a file at a given revision.

        This may be implemented by subclasses in order to support uploading
        binary files to diffs.

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
        raise NotImplementedError

    def get_file_size(
        self,
        *,
        filename: str,
        revision: str,
    ) -> int:
        """Return the size of a file at a given revision.

        This may optionally be implemented by subclasses if the SCM supports
        fetching file sizes.

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
        raise NotImplementedError
