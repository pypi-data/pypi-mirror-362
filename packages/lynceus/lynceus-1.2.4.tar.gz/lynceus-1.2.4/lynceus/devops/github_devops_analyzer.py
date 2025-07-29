from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import github
import requests
from github import Github, GithubObject, Permissions, UnknownObjectException
from github.PaginatedList import PaginatedList

from lynceus.core.exchange.lynceus_exchange import LynceusExchange
from lynceus.core.lynceus import LynceusSession
from lynceus.devops.devops_analyzer import DevOpsAnalyzer
from lynceus.utils import filter_kwargs
from lynceus.utils.lynceus_dict import LynceusDict


def github_exception_handler(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except github.GithubException as error:
            # Intercepts permission error.
            if error.status in (401, 403):
                raise PermissionError(
                    'You don\'t have enough permission to perform this operation on Github.') from error
            if error.status == 404:
                raise NameError('Unable to find requested Object.') from error

            # Raises any other error.
            raise

    return func_wrapper


def get_list_from_paginated_and_count(plist: PaginatedList, count: int | None = None):
    # Tries to return cut list according to specified count.
    try:
        if count is not None and count:
            return list(plist[:count])
    except IndexError:
        # Ignores IndexError, to returns the complete list, like if count was never specified.
        pass

    # Returns the complete list.
    return list(plist)


# Cf. https://pygithub.readthedocs.io/en/latest/introduction.html
# Cf. https://docs.github.com/en/rest
# Cf. https://pygithub.readthedocs.io/en/stable/changes.html#breaking-changes for 2.x version breaking changes (mainly on datetime which are no more naive).
# Important:
#  - the Gitlab group notion corresponds to Organization notion on Github
#  - the Team notion of Github is NOT managed
class GithubDevOpsAnalyzer(DevOpsAnalyzer):
    __manager: Github

    def __init__(self, lynceus_session: LynceusSession, uri: str, token: str, lynceus_exchange: LynceusExchange):
        super().__init__(lynceus_session, uri, 'github', lynceus_exchange)
        kwargs = {'auth': github.Auth.Token(token), 'timeout': 60}
        if uri:
            kwargs['base_url'] = uri

        self.__manager = Github(**kwargs)

    # The following methods are only for uniformity and coherence.
    def _extract_user_info(self, user) -> LynceusDict:
        return LynceusDict({
            'id': user.id,
            'name': user.name,
            'login': user.login,
            'username': user.login,
            'e-mail': user.email,
            'avatar_url': user.avatar_url,
            'bio': user.bio
        })

    def _extract_group_info(self, group) -> LynceusDict:
        return LynceusDict({
            'id': group.id,
            'name': group.name,
            # N.B.: it does not seem to be any "path" for Github organization
            'path': group.login
        })

    def _extract_project_info(self, project) -> LynceusDict:
        return LynceusDict({
            'id': project.id,
            'name': project.name,
            'path': project.full_name,
            'web_url': project.html_url
        })

    def _extract_member_info(self, member) -> LynceusDict:
        # In Github the corresponding notion is 'contributors', and there is no 'status' information.
        return LynceusDict({
            'id': member.id,
            'name': member.name,
            'login': member.login,
            'username': member.login,
            'parent_id': self.INFO_UNDEFINED,
            'state': self.STATUS_ACTIVE
        })

    def _extract_issue_event_info(self, issue_event, **kwargs) -> LynceusDict:
        return LynceusDict({
                               'id': issue_event.id,
                               'issue_id': issue_event.issue.number,
                               'action': issue_event.event,
                               'target_type': 'issue',
                               'created_at': issue_event.created_at,
                               'author': self.INFO_UNDEFINED if not issue_event.actor else issue_event.actor.name,
                               'title': issue_event.issue.title,
                               'issue_web_url': kwargs['project_web_url'] + f'/issues/{issue_event.issue.number}'

                               # N.B.: project information is unable, and must be added by caller via kwargs.
                           } | kwargs)

    def _extract_commit_info(self, commit) -> LynceusDict:
        return LynceusDict({
            'id': commit.sha,
            'short_id': commit.sha[:8],
            'parent_ids': [parent_commit.sha for parent_commit in commit.parents],
            'message': commit.raw_data['commit'].get('message'),
            'created_at': commit.commit.author.date,
            'author_name': commit.author.name,
            'author_email': commit.raw_data['commit']['author']['email'],
            'committer_name': commit.committer.name,
            'committer_email': commit.raw_data['commit']['committer']['email'],
        })

    def _extract_branch_info(self, branch) -> LynceusDict:
        return LynceusDict({
            'name': branch.name,
            'merged': len(branch.commit.parents) > 1,
            'commit_id': branch.commit.sha,
            'commit_short_id': branch.commit.sha[:8],
            'created_at': branch.commit.commit.author.date,
        })

    def _extract_tag_info(self, tag) -> LynceusDict:
        return LynceusDict({
            'name': tag.name,
            'commit_id': tag.commit.sha,
            'commit_short_id': tag.commit.sha[:8],
            'created_at': tag.commit.commit.author.date,
        })

    # The following methods are only performing read access on DevOps backend.
    @github_exception_handler
    def authenticate(self):
        # There is no direct authentication with Github,
        #  simply retrieves the current user to test it.
        self._do_get_current_user()

    @github_exception_handler
    def _do_get_current_user(self):
        return self.__manager.get_user()

    # pylint: disable=unused-argument
    @github_exception_handler
    def _do_get_user_without_cache(self, *, username: str = None, email: str = None, **kwargs):
        kwargs_filtered = filter_kwargs(args_filter=['user_id'], **kwargs)
        if kwargs_filtered:
            return self.__manager.get_user_by_id(**kwargs_filtered)

        return self.__manager.get_user(login=username)

    @github_exception_handler
    def _do_get_groups(self, *, count: int | None = None, **kwargs):
        return get_list_from_paginated_and_count(self.__manager.get_organizations(**kwargs), count)

    @github_exception_handler
    def _do_get_group_without_cache(self, *, full_path: str, **kwargs):
        # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html?highlight=organization#github.Repository.Repository.organization
        # https://pygithub.readthedocs.io/en/latest/github_objects/Team.html?highlight=organization#github.Team.Team.organization
        # https://pygithub.readthedocs.io/en/latest/examples/MainClass.html?highlight=organization#get-organization-by-name

        try:
            # There are no optional kwargs available in this implementation.
            return self.__manager.get_organization(full_path)
        except UnknownObjectException as exception:
            raise NameError(
                f'Group "{full_path}" has not been found.') from exception

    @github_exception_handler
    def _do_get_projects(self, *, count: int | None = None, **kwargs):
        return get_list_from_paginated_and_count(self._do_get_current_user().get_repos(**kwargs), count)

    @github_exception_handler
    def _do_get_project_without_cache(self, *, full_path: str, **kwargs):
        try:
            # There are no optional kwargs available in this implementation.
            return self.__manager.get_repo(full_path)
        except UnknownObjectException as exception:
            raise NameError(
                f'Project/repository "{full_path}" has not been found.') from exception

    @github_exception_handler
    def check_permissions_on_project(self, *, full_path: str, get_metadata: bool, pull: bool,
                                     push: bool = False, maintain: bool = False, admin: bool = False, **kwargs):
        try:
            # Retrieves repository metadata (can lead to NameError if authenticated user has not enough permissions).
            repository = self._do_get_project(full_path=full_path, **kwargs)

            # From here, we consider get_metadata permission is OK.

            # Checks others permissions.
            permissions: Permissions = repository.permissions
            if pull and not permissions.pull:
                return False

            if push and not permissions.push:
                return False

            if maintain and not permissions.maintain:
                return False

            if admin and not permissions.admin:
                return False

            # All permissions check are OK.
            return True
        except (PermissionError, NameError):
            # Returns True if there were NO permission at all to check ...
            return not get_metadata and not pull and not push and not maintain and not admin

    @github_exception_handler
    def _do_get_project_commits(self, *, full_path: str, git_ref_name: str, count: int | None = None, **kwargs):
        repository = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(repository.get_commits(sha=git_ref_name), count)

    @github_exception_handler
    def _do_get_project_branches(self, *, full_path: str, count: int | None = None, **kwargs):
        repository = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(repository.get_branches(), count)

    @github_exception_handler
    def _do_get_project_tags(self, *, full_path: str, count: int | None = None, **kwargs):
        repository = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(repository.get_tags(), count)

    @github_exception_handler
    def _do_get_project_members(self, *, full_path: str, count: int | None = None, **kwargs):
        repository = self._do_get_project(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(repository.get_contributors(**filter_kwargs(args_filter=['anon'], **kwargs)), count)

    @github_exception_handler
    def _do_get_group_members(self, *, full_path: str, count: int | None = None, **kwargs):
        # https://pygithub.readthedocs.io/en/latest/github_objects/Organization.html?highlight=member#github.Organization.Organization.get_members
        organization = self._do_get_group(full_path=full_path, **kwargs)
        return get_list_from_paginated_and_count(organization.get_members(**kwargs), count)

    @github_exception_handler
    def _do_get_project_issue_events(self, *, full_path: str, action: str | None = None,
                                     from_date: datetime | None = None,
                                     to_date: datetime | None = None,
                                     count: int | None = None, **kwargs):
        # https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types
        # https://docs.github.com/en/rest/activity/events

        repository = self._do_get_project(full_path=full_path, **kwargs)
        # Important: unfortunately it is NOT possible to filter on server side ...
        issue_events = get_list_from_paginated_and_count(repository.get_issues_events(), count)

        # Filters issue event according to specified parameter(s).
        for issue_event in issue_events:
            if action and issue_event.event != action:
                continue

            if from_date and issue_event.created_at < from_date:
                # Stops the iteration since this issue event is the first being too old.
                break

            if to_date and issue_event.created_at > to_date:
                # Ignores this issue event.
                continue

            yield issue_event

    @github_exception_handler
    def _do_get_project_issues(self, *, full_path: str, count: int | None = None, **kwargs):
        repository = self._do_get_project(full_path=full_path, **kwargs)

        
        if 'state' not in kwargs:
            kwargs['state'] = 'all'

        return get_list_from_paginated_and_count(repository.get_issues(**kwargs), count)

    @github_exception_handler
    def _do_get_project_merge_requests(self, *, full_path: str, count: int | None = None, **kwargs):
        repository = self._do_get_project(full_path=full_path, **kwargs)

        
        if 'state' not in kwargs:
            kwargs['state'] = 'all'

        return get_list_from_paginated_and_count(repository.get_pulls(**kwargs), count)

    @github_exception_handler
    def _do_get_project_milestones(self, *, full_path: str, count: int | None = None, **kwargs):
        repository = self._do_get_project(full_path=full_path, **kwargs)
        milestone_list = get_list_from_paginated_and_count(repository.get_milestones(**kwargs), count)
        return [milestone.title for milestone in milestone_list]

    @github_exception_handler
    def _do_get_group_milestones(self, *, full_path: str, count: int | None = None, **kwargs):
        self._logger.warning('There is no milestone on Organization under Github (you need to check milestones directly from a project/repository).')
        return []

    @github_exception_handler
    def _do_get_group_projects(self, *, full_path: str, count: int | None = None, **kwargs):
        organization = self._do_get_group(full_path=full_path, **kwargs)
        # Removes potential 'recursive' parameter which is not supported here.
        if 'recursive' in kwargs:
            del kwargs['recursive']
        return get_list_from_paginated_and_count(organization.get_repos(**kwargs), count)

    @github_exception_handler
    def get_user_stats_commit_activity(self, *, group_full_path: str = None, project_full_path: str = None,
                                       since: datetime = None, keep_empty_stats: bool = False, count: int | None = None):
        # Cf. https://developer.github.com/v3/repos/statistics/#get-the-last-year-of-commit-activity-data

        # Defines threshold date.
        contributions_since: datetime = since if since else datetime.now(tz=timezone.utc) - timedelta(days=365)
        stats_user_commit_activity: dict[date, int] = defaultdict(int)
        for repo in self._do_get_projects(count=count):
            for commit_activity in (repo.get_stats_commit_activity() or []):
                # TODO: define how to ensure it is the good author ?
                # if not current_user.name == commit_activity.author:
                #     print('TODO: remove // AUTHOR is NOT the same: ', current_user.name, commit_activity.author)
                #     continue

                # Ignores oldest statistics.
                if commit_activity.week < contributions_since:
                    continue

                # Ignores 0 stats but if wanted.
                if not keep_empty_stats and not commit_activity.total:
                    continue

                # For each stats.
                for day, commit_count in enumerate(commit_activity.days):
                    # Ignores 0 stats but if wanted.
                    if not keep_empty_stats and not commit_count:
                        continue

                    day_date = commit_activity.week + timedelta(days=day)
                    stats_user_commit_activity[day_date.date()] += commit_count

        return stats_user_commit_activity

    @github_exception_handler
    def get_user_contributions(self, *, since: datetime = None, keep_empty_stats: bool = False, count: int | None = None):
        # Cf. https://developer.github.com/v3/repos/statistics/

        # Defines threshold date.
        contributions_since: datetime = since if since else datetime.now(tz=timezone.utc) - timedelta(days=365)
        current_user = self._do_get_current_user()
        stats_user_contributions: dict[date, dict[str, int]] = {}
        for repo in self._do_get_projects(count=count):
            for contribution in (repo.get_stats_contributors() or []):
                if not current_user.name == contribution.author:
                    continue

                # For each stats.
                for stats in contribution.weeks:
                    # Ignores oldest statistics.
                    if stats.w < contributions_since:
                        continue

                    # Ignores 0 stats but if wanted.
                    if not keep_empty_stats and not stats.a and not stats.d and not stats.c:
                        continue

                    try:
                        stats_map = stats_user_contributions[stats.w.date()]
                    except KeyError:
                        stats_map = {'additions': 0, 'deletions': 0, 'commits': 0}
                        stats_user_contributions[stats.w.date()] = stats_map

                    stats_map['additions'] += stats.a
                    stats_map['deletions'] += stats.d
                    stats_map['commits'] += stats.c

        return stats_user_contributions

    @github_exception_handler
    def get_user_stats_code_frequency(self, *, count: int | None = None):
        stats_code_frequency = {}
        for repo in self._do_get_projects(count=count):
            for stats in (repo.get_stats_code_frequency() or []):
                try:
                    stats_map = stats_code_frequency[stats.week]
                except KeyError:
                    stats_map = {'additions': 0, 'deletions': 0}
                    stats_code_frequency[stats.week] = stats_map

                stats_map['additions'] += stats.additions
                stats_map['deletions'] += stats.deletions
        return stats_code_frequency

    @github_exception_handler
    def _do_download_repository(self, *, project_full_path: str, dest_path: Path,
                                reference: str = None, chunk_size: int = 1024, **kwargs):
        # Cf. https://developer.github.com/v3/repos/contents/#get-archive-link
        # Cf. https://github.com/PyGithub/PyGithub/blob/main/github/Repository.py#L1535
        repository = self._do_get_project(full_path=project_full_path, **kwargs)
        url: str = repository.get_archive_link(archive_format='tarball', ref=reference or GithubObject.NotSet)
        with requests.get(url, stream=True, timeout=60) as reader:
            # Ensures specified reference exists.
            if reader.status_code == 404:
                raise NameError(f'Reference "{reference}" does not exists for project/repository "{project_full_path}".')

            with open(dest_path, 'wb') as dest_file:
                for chunk in reader.iter_content(chunk_size=chunk_size):
                    dest_file.write(chunk)

    # The following methods are performing write/delete operation on DevOps backend.
    @github_exception_handler
    def _do_create_group(self, *, parent_group_full_path: str, new_group_name: str, new_group_relative_path: str, **kwargs):
        raise NotImplementedError('This feature is not available with the implementation for Github.')

    @github_exception_handler
    def _do_create_user(self, *, name: str, username: str, email: str, **kwargs):
        raise NotImplementedError('This feature is not available with the implementation for Github.')

    @github_exception_handler
    def _do_update_user_notification_settings(self, *, username: str, email: str, **kwargs):
        raise NotImplementedError('This feature is not available with the implementation for Github.')

    @github_exception_handler
    def _do_add_group_member(self, *, group_full_path: str, username: str, access, **kwargs):
        # https://pygithub.readthedocs.io/en/latest/github_objects/Team.html?highlight=member#github.Team.Team.add_to_members
        raise NotImplementedError('This feature is not available with the implementation for Github.')

    @github_exception_handler
    def _do_export_project(self, *, project_full_path: str, export_dst_full_path: Path, timeout_sec: int = 60, **kwargs):
        raise NotImplementedError('This feature is not available with the implementation for Github.')

    @github_exception_handler
    def _do_import_project(self, *, parent_group_full_path: str,
                           new_project_name: str, new_project_path: str,
                           import_src_full_path: Path, timeout_sec: int = 60, **kwargs):
        raise NotImplementedError('This feature is not available with the implementation for Github.')
