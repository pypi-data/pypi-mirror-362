import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

import gitlab
from gitlab.const import AccessLevel

from lynceus.core.config import DATETIME_FORMAT_SHORT
from lynceus.core.exchange.lynceus_exchange import LynceusExchange
from lynceus.core.lynceus import LynceusSession
from lynceus.devops.devops_analyzer import DevOpsAnalyzer
from lynceus.utils import flatten, parse_string_to_datetime
from lynceus.utils.lynceus_dict import LynceusDict


def gitlab_exception_handler(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except gitlab.exceptions.GitlabError as error:
            # Intercepts permission error.
            if error.response_code in (401, 403):
                raise PermissionError(
                    'You don\'t have enough permission to perform this operation on Gitlab.') from error
            if error.response_code == 404:
                raise NameError('Unable to find requested Object.') from error

            # Raises any other error.
            raise

    return func_wrapper


def get_list_from_paginated_and_count(plist_func: Callable, count: int | None = None, **kwargs):
    if count is not None and count:
        kwargs = {'per_page': count, 'page': 1} | kwargs
    else:
        kwargs = {'all': True} | kwargs

    return list(plist_func(**kwargs))


# Cf. https://python-gitlab.readthedocs.io/en/stable/api-usage.html
# Cf. https://docs.gitlab.com/ee/api/README.html
# Cf. https://docs.gitlab.com/ee/api/api_resources.html
class GitlabDevOpsAnalyzer(DevOpsAnalyzer):
    # Cf. https://docs.gitlab.com/ce/api/project_import_export.html#export-status
    # Cf. https://docs.gitlab.com/ce/api/project_import_export.html#import-status
    IMPORT_EXPORT_STATUS_SUCCESS: str = 'finished'
    IMPORT_EXPORT_STATUS_FAILED: str = 'failed'
    IMPORT_EXPORT_STATUS_NONE: str = 'none'

    def __init__(self, lynceus_session: LynceusSession, uri: str, token: str, lynceus_exchange: LynceusExchange):
        super().__init__(lynceus_session, uri, 'gitlab', lynceus_exchange)
        self.__manager = gitlab.Gitlab(uri, private_token=token)
        self.__current_token: dict | None = None

    # The following methods are only for uniformity and coherence.
    def _extract_user_info(self, user) -> LynceusDict:
        # Extracts information which are always available.
        user_info = {
            'id': user.id,
            'name': user.name,
            'login': user.username,
            'username': user.username
        }

        # Extracts extra information if available.
        for extra_info_key, extra_info_attr in ('e-mail', 'public_email'), ('avatar_url', 'avatar_url'), ('bio', 'bio'):
            value = user.attributes[extra_info_attr] if extra_info_attr in user.attributes else self.INFO_UNDEFINED
            user_info.update({extra_info_key: value})

        return LynceusDict(user_info)

    def _extract_group_info(self, group) -> LynceusDict:
        return LynceusDict({
            'id': group.id,
            'name': group.name,
            'path': group.full_path
        })

    def _extract_project_info(self, project) -> LynceusDict:
        return LynceusDict({
            'id': project.id,
            'name': project.name,
            'path': project.path_with_namespace,
            'web_url': project.web_url
        })

    def _extract_member_info(self, member) -> LynceusDict:
        member_info = {
            'id': member.id,
            'name': member.name,
            'login': member.username,
            'username': member.username,
            'state': member.state
        }

        # Extracts extra information if available.
        for extra_info_key, extra_info_attr in ('parent_id', 'group_id'), ('parent_id', 'project_id'):
            value = member.attributes[extra_info_attr] if extra_info_attr in member.attributes else None
            if value:
                member_info.update({extra_info_key: value})

        return LynceusDict(member_info)

    def _extract_issue_event_info(self, issue_event, **kwargs) -> LynceusDict:
        return LynceusDict({
                               'id': issue_event.id,
                               'issue_id': issue_event.target_iid,
                               'action': issue_event.action_name,
                               'target_type': issue_event.target_type,
                               'created_at': parse_string_to_datetime(datetime_str=issue_event.created_at),
                               'author': issue_event.author['name'],
                               'title': issue_event.target_title,
                               'issue_web_url': kwargs['project_web_url'] + f'/-/issues/{issue_event.target_iid}',

                               # N.B.: project information is unable, and must be added by caller via kwargs.
                           } | kwargs)

    def _extract_commit_info(self, commit) -> LynceusDict:
        return LynceusDict({
            'id': commit.id,
            'short_id': commit.short_id,
            'parent_ids': commit.parent_ids,
            'message': commit.message,
            'created_at': commit.created_at,
            'author_name': commit.author_name,
            'author_email': commit.author_email,
            'committer_name': commit.committer_name,
            'committer_email': commit.committer_email,
        })

    def _extract_branch_info(self, branch) -> LynceusDict:
        return LynceusDict({
            'name': branch.name,
            'merged': branch.merged,
            'commit_id': branch.commit['id'],
            'commit_short_id': branch.commit['short_id'],
            'created_at': parse_string_to_datetime(datetime_str=branch.commit['created_at']),
            # Not available for other DevOps: 'project_id': branch.project_id,
        })

    def _extract_tag_info(self, tag) -> LynceusDict:
        return LynceusDict({
            'name': tag.name,
            'commit_id': tag.commit['id'],
            'commit_short_id': tag.commit['short_id'],
            'created_at': parse_string_to_datetime(datetime_str=tag.commit['created_at']),
            # Not available for other DevOps: 'project_id': branch.project_id,
        })

    # The following methods are only performing read access on DevOps backend.
    @gitlab_exception_handler
    def authenticate(self):
        self.__manager.auth()

    @gitlab_exception_handler
    def _do_get_current_user(self):
        return self.__manager.user

    @gitlab_exception_handler
    def _do_get_user_without_cache(self, *, username: str = None, email: str = None, **kwargs):
        users = self.__manager.users.list(iterator=True, username=username, email=email, **kwargs)
        try:
            user = next(users)
            self._logger.debug(f'Successfully lookup user with parameters: "{username=}"/"{email=}".')
            return user
        except StopIteration:
            # pylint: disable=raise-missing-from
            raise NameError(
                f'User "{username=}"/"{email=}" has not been found with specified parameters ({kwargs if kwargs else "none"}).')

    @gitlab_exception_handler
    def _do_get_groups(self, *, count: int | None = None, **kwargs):
        return get_list_from_paginated_and_count(self.__manager.groups.list, count, **kwargs)

    @gitlab_exception_handler
    def _do_get_group_without_cache(self, *, full_path: str, **kwargs):
        groups = self.__manager.groups.list(iterator=True, search=full_path, search_namespaces=True, **kwargs)
        if not groups:
            raise NameError(
                f'Group "{full_path}" has not been found with specified parameters ({kwargs if kwargs else "none"}).')

        # Checks if match must be exact (which is now the case by default ... check if has been defined to False manually).
        if not bool(kwargs.get('exact_match', True)):
            if len(groups) > 1:
                self._logger.warning(f'There are more than one group matching requested path "{full_path}"' +
                                     f'(add "exact_match" parameter to ensure getting only one group): {groups} ')
            return next(groups)

        try:
            group = next(filter(lambda grp: str.lower(grp.full_path) == str.lower(full_path), groups))
            self._logger.debug(f'Successfully lookup group with full path "{full_path}".')
            return group
        except StopIteration:
            # pylint: disable=raise-missing-from
            raise NameError(
                f'Group "{full_path}" has not been found with specified parameters ({kwargs if kwargs else "none"}).' +
                f' Maybe you are looking for one of the following paths: {[group.full_path for group in groups]}')

    @gitlab_exception_handler
    def _do_get_projects(self, *, count: int | None = None, **kwargs):
        return get_list_from_paginated_and_count(self.__manager.projects.list, count, **kwargs)

    @gitlab_exception_handler
    def _do_get_project_without_cache(self, *, full_path: str, **kwargs):
        projects = self.__manager.projects.list(iterator=True, search=full_path, search_namespaces=True, **kwargs)
        try:
            project = next(projects)
            self._logger.debug(f'Successfully lookup project with full path "{full_path}".')
            return project
        except StopIteration:
            # pylint: disable=raise-missing-from
            raise NameError(
                f'Project "{full_path}" has not been found with specified parameters ({kwargs if kwargs else "none"}).')

    @gitlab_exception_handler
    def __get_current_token(self):
        if not self.__current_token:
            # Sample: {'id': 60, 'name': 'Lynceus CI/CD', 'revoked': False, 'created_at': '2020-10-22T15:50:13.516Z',
            #           'scopes': ['api', 'admin_mode'], 'user_id': 5, 'last_used_at': '2023-04-12T09:22:19.495Z',
            #           'active': True, 'expires_at': None}
            self.__current_token = self.__manager.personal_access_tokens.get('self')

        return self.__current_token

    @gitlab_exception_handler
    # pylint: disable=too-many-return-statements
    def check_permissions_on_project(self, *, full_path: str, get_metadata: bool, pull: bool,
                                     push: bool = False, maintain: bool = False, admin: bool = False, **kwargs):
        try:
            # First of all, checks get_metadata permission which is required anyway.
            _ = self._do_get_project(full_path=full_path, **kwargs)

            # From here, we consider get_metadata permission is OK.

            # Cf. https://docs.gitlab.com/ee/user/permissions.html
            # Cf. https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/lib/gitlab/access.rb#L12-18

            # Retrieves current use, and corresponding membership information if any, for specified project.
            current_user = self._do_get_current_user()
            members = self._do_get_project_members(full_path=full_path, recursive=True)

            member = next(filter(lambda grp: grp.id == current_user.id, members))
            access_level = member.access_level

            # According to my tests, required role (aka access_level):
            #  - at least REPORTER role to get access to repository metadata (name, tags, branches ...)
            #  - at least DEVELOPER role to be able to pull the repository (the read_repository scope is NOT enough here)
            #  - at least MAINTAINER role to get access to project statistics

            # Checks scopes of the token.
            token = self.__get_current_token()
            token_scopes = token.scopes
            api_scope = 'api' in token_scopes
            admin_scope = 'admin' in token_scopes
            read_repository_scope = 'read_repository' in token_scopes
            write_repository_scope = 'write_repository' in token_scopes

            if pull and ((not api_scope and not read_repository_scope) or access_level < AccessLevel.DEVELOPER):
                return False

            if push and ((not api_scope and not write_repository_scope) or access_level < AccessLevel.DEVELOPER):
                return False

            if maintain and ((not api_scope and not write_repository_scope) or access_level < AccessLevel.MAINTAINER):
                return False

            if admin and ((not api_scope and not admin_scope) or access_level < AccessLevel.OWNER):
                return False

            # All permission checks OK.
            return True
        except NameError:
            # Returns True if there were NO permission at all to check ...
            return not get_metadata and not pull and not push and not maintain and not admin
        except StopIteration:
            # Returns True if there were NO more permission to check ...
            return not pull and not push and not maintain and not admin

    @gitlab_exception_handler
    def _do_get_project_commits(self, *, full_path: str, git_ref_name: str, count: int | None = None, **kwargs):
        project = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(project.commits.list, count, ref_name=git_ref_name, **kwargs)

    @gitlab_exception_handler
    def _do_get_project_branches(self, *, full_path: str, count: int | None = None, **kwargs):
        project = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(project.branches.list, count, **kwargs)

    @gitlab_exception_handler
    def _do_get_project_tags(self, *, full_path: str, count: int | None = None, **kwargs):
        project = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(project.tags.list, count, **kwargs)

    @gitlab_exception_handler
    def _do_get_project_members(self, *, full_path: str, count: int | None = None, **kwargs):
        project = self._do_get_project(full_path=full_path, **kwargs)

        if not bool(kwargs.get('recursive', False)):
            return get_list_from_paginated_and_count(project.members.list, count, **kwargs)

        return get_list_from_paginated_and_count(project.members_all.list, count, **kwargs)

    @gitlab_exception_handler
    def _do_get_group_members(self, *, full_path: str, count: int | None = None, **kwargs):
        group = self._do_get_group(full_path=full_path, **kwargs)

        if not bool(kwargs.get('recursive', False)):
            return get_list_from_paginated_and_count(group.members.list, count, **kwargs)

        return get_list_from_paginated_and_count(group.members_all.list, count, **kwargs)

    @gitlab_exception_handler
    def _do_get_project_issue_events(self, *, full_path: str, action: str | None = None,
                                     from_date: datetime | None = None,
                                     to_date: datetime | None = None, count: int | None = None, **kwargs):
        # Cf. https://python-gitlab.readthedocs.io/en/stable/api/gitlab.v4.html?highlight=events#gitlab.v4.objects.ProjectEventManager
        # Object listing filters
        #   action => https://docs.gitlab.com/ee/user/profile/index.html#user-contribution-events
        #   target_type => https://docs.gitlab.com/ee/api/events.html#target-types
        #   sort
        project = self._do_get_project(full_path=full_path, **kwargs)

        # Adds filters if needed.
        if action:
            kwargs['action'] = action

        #   before & after => https://docs.gitlab.com/ee/api/events.html#date-formatting
        if from_date:
            kwargs['after'] = from_date.strftime('%Y-%m-%d')

        if to_date:
            kwargs['before'] = to_date.strftime('%Y-%m-%d')

        return get_list_from_paginated_and_count(project.events.list, count, target_type='issue', **kwargs)

    @gitlab_exception_handler
    def _do_get_project_issues(self, *, full_path: str, count: int | None = None, **kwargs):
        project = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(project.issues.list, count, **kwargs)

    @gitlab_exception_handler
    def _do_get_project_merge_requests(self, *, full_path: str, count: int | None = None, **kwargs):
        project = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(project.mergerequests.list, count, **kwargs)

    @gitlab_exception_handler
    def _do_get_project_milestones(self, *, full_path: str, count: int | None = None, **kwargs):
        project = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(project.milestones.list, count, **kwargs)

    @gitlab_exception_handler
    def __get_recursive_groups(self, *, full_path: str, count: int | None = None, **kwargs):
        # TODO: find a way to implement count properly.
        group = self._do_get_group(full_path=full_path, **kwargs)
        subgroups = get_list_from_paginated_and_count(group.subgroups.list, count, **kwargs)
        if not subgroups:
            return [group]
        return flatten(self.__get_recursive_groups(full_path=subgroup.full_path, **kwargs) for subgroup in subgroups)

    @gitlab_exception_handler
    def _do_get_group_projects(self, *, full_path: str, count: int | None = None, **kwargs):
        group = self._do_get_group(full_path=full_path, **kwargs)

        # Checks if recursive is requested.
        if not bool(kwargs.get('recursive', False)):
            project_list = get_list_from_paginated_and_count(group.projects.list, count, **kwargs)
        else:
            # TODO: find a way to implement count
            all_groups = {group} | set(self.__get_recursive_groups(full_path=full_path, **kwargs))
            project_list = flatten(group.projects.list(all=True) for group in all_groups)

        return list(map(lambda gp: self._do_get_project(full_path=gp.path_with_namespace), project_list))

    @gitlab_exception_handler
    def _do_get_group_milestones(self, *, full_path: str, count: int | None = None, **kwargs):
        group = self._do_get_group(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(group.milestones.list, count, **kwargs)

    @gitlab_exception_handler
    def get_user_stats_commit_activity(self, *, group_full_path: str = None, project_full_path: str = None,
                                       since: datetime = None, keep_empty_stats: bool = False, count: int | None = None):
        # TODO: find a way to implement count
        # Cf. https://docs.gitlab.com/ee/api/project_statistics.html#get-the-statistics-of-the-last-30-days

        # Defines projects on which to perform statistics.
        if group_full_path is None:
            projects = self._do_get_projects(count=count)
        else:
            projects = self._do_get_group_projects(full_path=group_full_path, count=count)
            if project_full_path is not None:
                projects.append(self._do_get_project(full_path=project_full_path))

        # Defines threshold date.
        contributions_since: datetime = since if since else datetime.now(tz=timezone.utc) - timedelta(days=365)
        stats_user_commit_activity: dict[datetime.date, int] = defaultdict(int)
        for _project in projects:
            for commit_activity in _project.additionalstatistics.get().fetches['days']:
                day_date = parse_string_to_datetime(datetime_str=commit_activity['date'], datetime_format=DATETIME_FORMAT_SHORT)

                # Ignores oldest statistics.
                if day_date < contributions_since:
                    continue

                # Ignores 0 stats but if wanted.
                if not keep_empty_stats and not commit_activity['count']:
                    continue

                stats_user_commit_activity[day_date.date()] += commit_activity['count']

        return stats_user_commit_activity

    @gitlab_exception_handler
    # pylint: disable=unused-argument
    def get_user_contributions(self, *, since: datetime = None, keep_empty_stats: bool = False, count: int | None = None):
        self._logger.warning('get_user_contributions is not implemented yet for GitLab DevOps Analyzer')
        return {}

    @gitlab_exception_handler
    def get_user_stats_code_frequency(self, *, count: int | None = None):
        self._logger.warning(
            'get_user_stats_commit_activity is not implemented yet for GitLab DevOps Analyzer')
        return {}

    @gitlab_exception_handler
    def _do_download_repository(self, *, project_full_path: str, dest_path: Path,
                                reference: str = None, chunk_size: int = 1024, **kwargs):
        # Cf. https://docs.gitlab.com/ee/api/repositories.html#get-file-archive
        # Cf. https://github.com/python-gitlab/python-gitlab/blob/main/gitlab/v4/objects.py#L4465
        project = self._do_get_project(full_path=project_full_path, **kwargs)
        with open(dest_path, 'wb') as dest_file:
            project.repository_archive(sha=reference, streamed=True, action=dest_file.write, chunk_size=chunk_size,
                                       **kwargs)

    # The following methods are performing write/delete operation on DevOps backend.
    @gitlab_exception_handler
    def _do_create_group(self, *, parent_group_full_path: str, new_group_name: str, new_group_relative_path: str, **kwargs):
        # Prepares the common parameters.
        group_create_params: dict[str, str] = {'name': new_group_name,
                                               'path': new_group_relative_path,
                                               **kwargs}

        # Checks if the group must be created under an existing one.
        if parent_group_full_path:
            root_group = self._do_get_group(full_path=parent_group_full_path, exact_match=True)
            if not root_group:
                raise NameError(f'Unable to find the parent group with name "{parent_group_full_path}".')

            # Adds the parent parameter.
            group_create_params.update({'parent_id': root_group.id})

        # Cf. https://docs.gitlab.com/ee/api/groups.html#new-group
        # Requests group creation.
        return self.__manager.groups.create(group_create_params)

    @gitlab_exception_handler
    def _do_create_user(self, *, name: str, username: str, email: str, **kwargs):
        # Cf. https://python-gitlab.readthedocs.io/en/stable/gl_objects/users.html
        return self.__manager.users.create(
            {
                'name': name,
                'username': username,
                'email': email,
                'reset_password': True,
                **kwargs})

    @gitlab_exception_handler
    def _do_update_user_notification_settings(self, *, username: str, email: str, **kwargs):
        # Cf. https://python-gitlab.readthedocs.io/en/stable/gl_objects/notifications.html

        # N.B.: in Gitlab, only the notification settings of the authenticated user can be updated.
        # so here, to update the settings of the specified user, we need to request a dedicated impersonation token.
        # Cf. https://python-gitlab.readthedocs.io/en/stable/gl_objects/users.html?highlight=impersonation#user-impersonation-tokens
        user = self._do_get_user(username=username, email=email)

        # Creates a new impersonation token.
        user_active_impersonation_tokens = user.impersonationtokens.list(state='active')
        self._logger.debug(f'Looking for existing "active" impersonation token for user "{self._extract_user_info(user)}": "{user_active_impersonation_tokens=}".')
        impersonation_token = user.impersonationtokens.create({'name': 'notif_token', 'scopes': ['api']})
        self._logger.debug(f'Successfully created new impersonation token for user "{self._extract_user_info(user)}": "{impersonation_token=}".')

        # Creates a new dedicated Gitlab manager, to update the settings.
        user_gl = gitlab.Gitlab(self._uri, private_token=impersonation_token.token)
        user_notificationsettings = user_gl.notificationsettings.get()
        self._logger.debug(f'These are the current user notification settings: "{user_notificationsettings.attributes=}".')

        # Updates notification settings.
        for setting, value in kwargs.items():
            self._logger.debug(f'Updating user notification settings "{setting}" to "{value}".')
            setattr(user_notificationsettings, setting, value)
        user_notificationsettings.save()
        self._logger.debug(f'Successfully updated user notification settings to: "{user_notificationsettings.attributes=}".')

        # Cleans the impersonation token.
        impersonation_token.delete()
        del user_gl

        # Returns the User which may hold some interesting information in some DevOps Backend implementation.
        return user

    @gitlab_exception_handler
    def _do_add_group_member(self, *, group_full_path: str, username: str, access, **kwargs):
        group = self._do_get_group(full_path=group_full_path, exact_match=True)
        user = self._do_get_user(username=username)

        return group.members.create(
            {'user_id': user.id,
             'access_level': access,
             **kwargs})

    def __wait_until_status_or_timeout(self, *, obj, refresh_func, attr_name: str, values: list[str], timeout_sec: int, step_sec: int = 2):
        self._logger.debug(f'Starting polling wait until maximum of {timeout_sec} seconds, for attributes "{attr_name=}" on "{obj=}" to reach one of the "{values=}" ...')
        remaining_time: int = timeout_sec
        refresh_func(obj)
        while remaining_time > 0 and getattr(obj, attr_name) not in values:
            time.sleep(step_sec)
            remaining_time -= step_sec
            refresh_func(obj)

        self._logger.debug(f'Attribute "{attr_name=}" on "{obj=}" reached "{getattr(obj, attr_name)}", in "{timeout_sec - remaining_time}" seconds.')

    @gitlab_exception_handler
    def _do_export_project(self, *, project_full_path: str, export_dst_full_path: Path, timeout_sec: int = 60, **kwargs):
        # Cf. https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html#import-export
        # Cf. https://docs.gitlab.com/ce/api/project_import_export.html

        # Safe-guard: prepares output structure.
        export_dst_full_path.parent.mkdir(parents=True, exist_ok=True)

        # Create the export.
        self._logger.info(f'Requesting export of project with full path "{project_full_path}" ...')
        project = self._do_get_project(full_path=project_full_path)
        export = project.exports.create()

        # Waits till the export reaches a final status.
        self.__wait_until_status_or_timeout(obj=export,
                                            refresh_func=lambda instance: instance.refresh(),
                                            attr_name='export_status',
                                            values=[self.IMPORT_EXPORT_STATUS_SUCCESS, self.IMPORT_EXPORT_STATUS_FAILED],
                                            timeout_sec=timeout_sec)

        # Checks status.
        if export.export_status != self.IMPORT_EXPORT_STATUS_SUCCESS:
            raise ValueError(f'Export of project with full path "{project_full_path}" did not reach' +
                             f' "{self.IMPORT_EXPORT_STATUS_SUCCESS}" success status, in "{timeout_sec}" seconds' +
                             f' but "{export.export_status}".')

        # Saves the result.
        self._logger.debug(f'Export is now ready, saving it to "{export_dst_full_path}" ...')
        with open(export_dst_full_path, 'wb') as export_file:
            export.download(streamed=True, action=export_file.write)
        self._logger.info(f'Successfully exported project with full path "{project_full_path}" to "{export_dst_full_path}".')

    @gitlab_exception_handler
    def _do_import_project(self, *, parent_group_full_path: str,
                           new_project_name: str, new_project_path: str,
                           import_src_full_path: Path, timeout_sec: int = 60, **kwargs):
        # Cf. https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html#import-export
        # Cf. https://docs.gitlab.com/ce/api/project_import_export.html

        # Safe-guard: ensures import source file exists..
        if not import_src_full_path.exists():
            raise ValueError(f'Specified source file "{import_src_full_path}" does not exist. Aborting import.')

        # Create the import.
        project_complete_path = new_project_path if not parent_group_full_path else f'{parent_group_full_path}/{new_project_path}'
        self._logger.info(f'Requesting import of project "{import_src_full_path}" to new project with full path "{project_complete_path}" ...')

        with open(import_src_full_path, 'rb') as file_source:
            output = self.__manager.projects.import_project(
                file_source,
                namespace=parent_group_full_path,
                path=new_project_path, name=new_project_name,
                **kwargs)
        new_project = self.__manager.projects.get(output['id'])
        project_import = new_project.imports.get()

        # Waits till the import reaches a final status.
        self.__wait_until_status_or_timeout(obj=project_import,
                                            refresh_func=lambda instance: instance.refresh(),
                                            attr_name='import_status',
                                            values=[self.IMPORT_EXPORT_STATUS_SUCCESS, self.IMPORT_EXPORT_STATUS_FAILED],
                                            timeout_sec=timeout_sec)

        # Checks status.
        if project_import.import_status != self.IMPORT_EXPORT_STATUS_SUCCESS:
            raise ValueError(f'Import of "{import_src_full_path}" to new project with full path "{new_project.path_with_namespace}" did not reach' +
                             f' "{self.IMPORT_EXPORT_STATUS_SUCCESS}" success status, in "{timeout_sec}" seconds' +
                             f' but "{project_import.import_status}".')

        self._logger.info(f'Successfully imported "{import_src_full_path}" to new project with full path "{new_project.path_with_namespace}" ...')
