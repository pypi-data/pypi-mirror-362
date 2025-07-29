from datetime import datetime
from pathlib import Path

from lynceus.core.exchange.lynceus_exchange import LynceusExchange
from lynceus.core.lynceus import LynceusSession
from lynceus.core.lynceus_client import LynceusClientClass
from lynceus.utils.lynceus_dict import LynceusDict


# TODO: add members?
# TODO: add accessrequests/permissions listing feature


# pylint: disable=too-many-public-methods
class DevOpsAnalyzer(LynceusClientClass):
    STATUS_ACTIVE: str = 'active'
    INFO_UNDEFINED: str = 'undefined'

    CACHE_USER_TYPE: str = 'user'
    CACHE_GROUP_TYPE: str = 'group'
    CACHE_PROJECT_TYPE: str = 'project'

    def __init__(self, lynceus_session: LynceusSession, uri: str, logger_name: str, lynceus_exchange: LynceusExchange):
        super().__init__(lynceus_session, logger_name, lynceus_exchange)
        self._uri = uri

        # Initializes cache system.
        self.__cache = {
            self.CACHE_USER_TYPE: {},
            self.CACHE_GROUP_TYPE: {},
            self.CACHE_PROJECT_TYPE: {},
        }

    # The following methods are only for uniformity and coherence.
    def _extract_user_info(self, user) -> LynceusDict:
        raise NotImplementedError()

    def _extract_group_info(self, group) -> LynceusDict:
        raise NotImplementedError()

    def _extract_project_info(self, project) -> LynceusDict:
        raise NotImplementedError()

    def _extract_member_info(self, member) -> LynceusDict:
        raise NotImplementedError()

    def _extract_issue_event_info(self, issue_event, **kwargs) -> LynceusDict:
        raise NotImplementedError()

    def _extract_commit_info(self, commit) -> LynceusDict:
        raise NotImplementedError()

    def _extract_branch_info(self, branch) -> str:
        raise NotImplementedError()

    def _extract_tag_info(self, tag) -> str:
        raise NotImplementedError()

    def __get_from_cache(self, *, cache_type: str, cache_key, log_access: bool = True):
        if log_access:
            self._logger.debug(f'Checking if an instance is registered in cache, for type "{cache_type}" and key "{cache_key}".')
        return self.__cache[cache_type].get(cache_key, None)

    def __register_in_cache(self, *, cache_type: str, cache_key, obj, obj_short):
        # Safe-guard: checks if it has already been registered in cache.
        from_cache = self.__get_from_cache(cache_type=cache_type, cache_key=cache_key, log_access=False)
        if from_cache:
            self._logger.warning(f'An instance of type "{cache_type}" has already been registered in cache, for key "{cache_key}". It will be overridden.')

        self._logger.debug(f'Registering a complete/long instance of type "{cache_type}" in cache, for key "{cache_key}", whose short version is: "{obj_short}".')
        self.__cache[cache_type][cache_key] = obj

    # The following methods are only performing read access on DevOps backend.
    def authenticate(self):
        raise NotImplementedError()

    def _do_get_current_user(self):
        raise NotImplementedError()

    def get_current_user(self):
        self._logger.debug('Retrieving current user information.')
        user = self._do_get_current_user()

        return self._extract_user_info(user)

    def _do_get_user_without_cache(self, *, username: str = None, email: str = None, **kwargs):
        raise NotImplementedError()

    def _do_get_user(self, *, username: str = None, email: str = None, **kwargs):
        # Checks if available in cache.
        cache_key = (username, email)
        user = self.__get_from_cache(cache_type=self.CACHE_USER_TYPE, cache_key=cache_key)

        # Retrieves it if not available in cache.
        if not user:
            user = self._do_get_user_without_cache(username=username, email=email, **kwargs)

            # Registers in cache.
            self.__register_in_cache(cache_type=self.CACHE_USER_TYPE, cache_key=cache_key,
                                     obj=user, obj_short=self._extract_user_info(user))

        return user

    def get_user(self, *, username: str = None, email: str = None, **kwargs):
        self._logger.debug(f'Retrieving user "{username=}" with "{email}" ({kwargs=}).')
        user = self._do_get_user(username=username, email=email, **kwargs)
        return self._extract_user_info(user)

    def _do_get_groups(self, *, count: int | None = None, **kwargs):
        raise NotImplementedError()

    def get_groups(self, *, count: int | None = None, **kwargs):
        self._logger.debug(f'Retrieving groups ({count=}; {kwargs=}).')
        groups = self._do_get_groups(count=count, **kwargs)
        return [self._extract_group_info(group) for group in groups]

    def _do_get_group_without_cache(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def _do_get_group(self, *, full_path: str, **kwargs):
        # Checks if available in cache.
        cache_key = (full_path,)
        group = self.__get_from_cache(cache_type=self.CACHE_GROUP_TYPE, cache_key=cache_key)

        # Retrieves it if not available in cache.
        if not group:
            group = self._do_get_group_without_cache(full_path=full_path, **kwargs)

            # Registers in cache.
            self.__register_in_cache(cache_type=self.CACHE_GROUP_TYPE, cache_key=cache_key,
                                     obj=group, obj_short=self._extract_group_info(group))

        return group

    def get_group(self, *, full_path: str, **kwargs):
        self._logger.debug(f'Retrieving group "{full_path=}" ({kwargs=}).')
        group = self._do_get_group(full_path=full_path, **kwargs)
        return self._extract_group_info(group)

    def _do_get_projects(self, **kwargs):
        raise NotImplementedError()

    def get_projects(self, **kwargs):
        self._logger.debug(f'Retrieving projects ({kwargs=}).')
        projects = self._do_get_projects(**kwargs)
        return [self._extract_project_info(project) for project in projects]

    def _do_get_project_without_cache(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def _do_get_project(self, *, full_path: str, **kwargs):
        # Checks if available in cache.
        cache_key = (full_path,)
        project = self.__get_from_cache(cache_type=self.CACHE_PROJECT_TYPE, cache_key=cache_key)

        # Retrieves it if not available in cache.
        if not project:
            project = self._do_get_project_without_cache(full_path=full_path, **kwargs)

            # Registers in cache.
            self.__register_in_cache(cache_type=self.CACHE_PROJECT_TYPE, cache_key=cache_key,
                                     obj=project, obj_short=self._extract_project_info(project))

        return project

    def get_project(self, *, full_path: str, **kwargs):
        self._logger.debug(f'Retrieving project "{full_path=}" ({kwargs=}).')
        project = self._do_get_project(full_path=full_path, **kwargs)
        return self._extract_project_info(project)

    def check_permissions_on_project(self, *, full_path: str, get_metadata: bool, pull: bool,
                                     push: bool = False, maintain: bool = False, admin: bool = False, **kwargs):
        """
        Checks permission of Authenticated user on specific project (full_path and optional kwargs).

        :param full_path: full path of the project (including namespace)
        :param get_metadata: check 'get project metadata' permission.
        :param pull: check 'pull' permission.
        :param push: check 'push' permission (does not check this permission by default).
        :param maintain: check 'maintain' permission (does not check this permission by default).
        :param admin: check 'admin' permission (does not check this permission by default).
        :param kwargs: optional additional parameters
        :return: True if the Authenticated user has requested permission, False otherwise.
        """
        raise NotImplementedError()

    def _do_get_project_members(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def get_project_commits(self, *, full_path: str, git_ref_name: str, count: int | None = None, **kwargs):
        self._logger.debug(f'Retrieving commits from git_reference "{git_ref_name}" of project "{full_path}".')
        commits = self._do_get_project_commits(full_path=full_path, git_ref_name=git_ref_name, count=count, **kwargs)
        return [self._extract_commit_info(commit) for commit in commits]

    def _do_get_project_commits(self, *, full_path: str, git_ref_name: str, count: int | None = None, **kwargs):
        raise NotImplementedError()

    def get_project_branches(self, *, full_path: str, **kwargs):
        self._logger.debug(f'Retrieving branches of project "{full_path=}" ({kwargs=}).')
        branches = self._do_get_project_branches(full_path=full_path, **kwargs)
        return [self._extract_branch_info(branch) for branch in branches]

    def _do_get_project_branches(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def get_project_tags(self, *, full_path: str, **kwargs):
        self._logger.debug(f'Retrieving tags of project "{full_path=}" ({kwargs=}).')
        tags = self._do_get_project_tags(full_path=full_path, **kwargs)
        return [self._extract_tag_info(tag) for tag in tags]

    def _do_get_project_tags(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def get_project_members(self, *, full_path: str, **kwargs):
        """
        Return all members of project.

        :param full_path: full path of the project (including namespace)
        :return: all members of the project
        """
        self._logger.debug(f'Retrieving members of project "{full_path=}" ({kwargs=}).')
        project_members = self._do_get_project_members(full_path=full_path, **kwargs)
        return [self._extract_member_info(member) for member in project_members]

    def _do_get_group_members(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def get_group_members(self, *, full_path: str, **kwargs):
        """
        Return all members of group (aka Organization).

        :param full_path: full path of the group (including namespace)
        :return: all members of the group
        """
        self._logger.debug(f'Retrieving members of group "{full_path=}" ({kwargs=}).')
        members = self._do_get_group_members(full_path=full_path, **kwargs)
        return [self._extract_member_info(member) for member in members]

    def _do_get_project_issue_events(self, *, full_path: str, action: str | None = None,
                                     from_date: datetime | None = None,
                                     to_date: datetime | None = None, **kwargs):
        raise NotImplementedError()

    def get_project_issue_events(self, *, full_path: str, action: str | None = None,
                                 from_date: datetime | None = None,
                                 to_date: datetime | None = None, **kwargs):
        """
        Returns project issue events (filtered according to specified parameters).

        :param full_path: path of the project (including namespace)
        :param action: optional issue event action to filter on, most of them are common to DevOps
                See this one for Gitlab specs: https://docs.gitlab.com/ee/user/profile/index.html#user-contribution-events
                See this one for Github specs: https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types#event-payload-object-6
        :param from_date: optional datetime from which to consider issue events
        :param to_date: optional datetime until which to consider issue events
        :param kwargs: optional additional parameters
        :return: filtered issue events of the project.
        """
        self._logger.debug(f'Retrieving issue events of project "{full_path=}" ({action=}; {from_date=}; {to_date=}; {kwargs=}).')
        project_events = self._do_get_project_issue_events(full_path=full_path, action=action, from_date=from_date, to_date=to_date, **kwargs)

        # Important: in Github there is no project (either id or name) information attached to event, and on Gitlab there is only the id.
        # To return consistent result, we add both here.
        project = self.get_project(full_path=full_path)
        project_metadata = {
            'project_id': project.id,
            'project_name': project.name,
            'project_web_url': project.web_url,
        }

        return [self._extract_issue_event_info(event, **project_metadata) for event in project_events]

    def _do_get_project_issues(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def get_project_issues(self, *, full_path: str, **kwargs):
        """
        Return all issues of project.

        :param full_path: path of the project (including namespace)
        :return: all issues of the project
        """
        self._logger.debug(f'Retrieving issues of project "{full_path=}" {kwargs=}).')
        return self._do_get_project_issues(full_path=full_path, **kwargs)

    def get_project_pull_requests(self, *, full_path: str, **kwargs):
        return self.get_project_merge_requests(full_path=full_path, **kwargs)

    def _do_get_project_merge_requests(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def get_project_merge_requests(self, *, full_path: str, **kwargs):
        """
        Return all issues of project.

        :param full_path: path of the project (including namespace)
        :return: all issues of the project
        """
        self._logger.debug(f'Retrieving merge/pull requests of project "{full_path=}" {kwargs=}).')
        return self._do_get_project_merge_requests(full_path=full_path, **kwargs)

    def _do_get_project_milestones(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def get_project_milestones(self, *, full_path: str, **kwargs):
        """
        Return all milestones (aka sprints) of project.

        :param full_path: path of the project (including namespace)
        :return: all milestones of the project
        """
        self._logger.debug(f'Retrieving milestones of project "{full_path=}" {kwargs=}).')
        return self._do_get_project_milestones(full_path=full_path, **kwargs)

    def _do_get_group_projects(self, *, full_path: str, **kwargs):
        """
        Return all projects of group.

        :param full_path: path of the group
        :return: all projects of the group
        """
        raise NotImplementedError()

    def get_group_projects(self, *, full_path: str, **kwargs):
        self._logger.debug(f'Retrieving projects of group "{full_path=}" ({kwargs=}).')
        projects = self._do_get_group_projects(full_path=full_path, **kwargs)
        return [self._extract_project_info(project) for project in projects]

    def _do_get_group_milestones(self, *, full_path: str, **kwargs):
        raise NotImplementedError()

    def get_group_milestones(self, *, full_path: str, **kwargs):
        """
        Return all milestones (aka sprints) of group.

        :param full_path: path of the group
        :return: all milestones of the group
        """
        self._logger.debug(f'Retrieving milestones of group "{full_path=}" {kwargs=}).')
        return self._do_get_group_milestones(full_path=full_path, **kwargs)

    def get_user_stats_commit_activity(self, *, group_full_path: str = None, project_full_path: str = None,
                                       since: datetime = None, keep_empty_stats: bool = False):

        """
        Computes total statistics of all accessible projects of authenticated user, or all projects of specified group
         and/or of specified project.
        :param group_full_path: (optional) statistics will be computed on all projects of this group.
        :param project_full_path: (optional) statistics will be computed on this project.
        :param since: start date from which statistics must be computed.
        :param keep_empty_stats:
        """
        raise NotImplementedError()

    def get_user_contributions(self, *, since: datetime = None, keep_empty_stats: bool = False):
        raise NotImplementedError()

    def get_user_stats_code_frequency(self):
        raise NotImplementedError()

    def download_repository(self, *, project_full_path: str, dest_path: Path, reference: str = None,
                            chunk_size: int = 1024, **kwargs):
        self._logger.debug(f'Starting repository download of project "{project_full_path}" with git reference "{reference}", to destination file "{dest_path}" ...')
        try:
            self._do_download_repository(project_full_path=project_full_path, dest_path=dest_path, reference=reference, chunk_size=chunk_size, **kwargs)
            self._logger.info(f'Successfully downloaded repository of project "{project_full_path}" with git reference "{reference}", to destination file "{dest_path}".')
        except NameError as exc:
            
            
            #  like with hacked wrapper/2022-wrapper-lynceus-test.conf
            git_reference_str: str = f'git reference "{reference}"' if reference is not None else 'default git reference'
            error_message: str = f'Unable to download/access {git_reference_str} of project "{project_full_path}" (ensure your Token has permissions enough).'
            self._logger.warning(error_message)
            raise ValueError(error_message) from exc

    def _do_download_repository(self, *, project_full_path: str, dest_path: Path, reference: str = None,
                                chunk_size: int = 1024, **kwargs):
        raise NotImplementedError()

    # The following methods are performing write/delete operation on DevOps backend.
    def _do_create_group(self, *, parent_group_full_path: str, new_group_name: str, new_group_relative_path: str, **kwargs):
        """
        Create a new group.

        :param parent_group_full_path: full path of the parent group in which to create this new group, None to create a new root group.
        :param new_group_name: name of the group to create.
        :param new_group_relative_path: path of the group to create, relative to its optional parent group.
        :param kwargs: any optional parameters (e.g. visibility, project_creation_level ...)
        :return: an usable presentation of the created group.
        """
        raise NotImplementedError()

    def create_group(self, *, parent_group_full_path: str, new_group_name: str, new_group_relative_path: str, **kwargs):
        self._logger.debug(f'Creating group "{new_group_name=}" ({parent_group_full_path=}; {new_group_relative_path=}; {kwargs=}).')
        group = self._do_create_group(parent_group_full_path=parent_group_full_path, new_group_name=new_group_name,
                                      new_group_relative_path=new_group_relative_path, **kwargs)
        return self._extract_group_info(group)

    def _do_create_user(self, *, name: str, username: str, email: str, **kwargs):
        raise NotImplementedError()

    def create_user(self, *, name: str, username: str, email: str, **kwargs):
        self._logger.debug(f'Creating user "{name=}" ({username=}; {email=}; {kwargs=}).')
        user = self._do_create_user(name=name, username=username, email=email, **kwargs)
        return self._extract_user_info(user)

    def _do_update_user_notification_settings(self, *, username: str, email: str, **kwargs):
        raise NotImplementedError()

    def update_user_notification_settings(self, *, username: str, email: str, **kwargs):
        self._logger.debug(f'Updating notification settings for "{username=}" ({email=}; {kwargs=}).')
        user = self._do_update_user_notification_settings(username=username, email=email, **kwargs)
        return self._extract_user_info(user)

    def _do_add_group_member(self, *, group_full_path: str, username: str, access, **kwargs):
        raise NotImplementedError()

    def add_group_member(self, *, group_full_path: str, username: str, access, **kwargs):
        self._logger.debug(f'Adding user "{username=}" as member of group "{group_full_path=} ({access=}; {kwargs=}).')
        member = self._do_add_group_member(group_full_path=group_full_path, username=username, access=access, **kwargs)
        return self._extract_member_info(member)

    def _do_export_project(self, *, project_full_path: str, export_dst_full_path: Path, timeout_sec: int = 60, **kwargs):
        raise NotImplementedError()

    def export_project(self, *, project_full_path: str, export_dst_full_path: Path, timeout_sec: int = 60, **kwargs):
        self._logger.debug(f'Exporting project "{project_full_path=}" ({export_dst_full_path=}; {timeout_sec=}; {kwargs=}).')
        return self._do_export_project(project_full_path=project_full_path,
                                       export_dst_full_path=export_dst_full_path,
                                       timeout_sec=timeout_sec, **kwargs)

    def _do_import_project(self, *, parent_group_full_path: str,
                           new_project_name: str, new_project_path: str,
                           import_src_full_path: Path, timeout_sec: int = 60, **kwargs):
        raise NotImplementedError()

    def import_project(self, *, parent_group_full_path: str,
                       new_project_name: str, new_project_path: str,
                       import_src_full_path: Path, timeout_sec: int = 60, **kwargs):
        self._logger.debug(f'Importing project "{new_project_path=}" ({parent_group_full_path=}; {new_project_name=}; {import_src_full_path=}; {timeout_sec=}; {kwargs=}).')
        return self._do_import_project(parent_group_full_path=parent_group_full_path,
                                       new_project_name=new_project_name, new_project_path=new_project_path,
                                       import_src_full_path=import_src_full_path,
                                       timeout_sec=timeout_sec, **kwargs)
