"""
File with class to work with Ximc Redmine.
"""

import re
from typing import Callable, Dict, Iterable, List, Optional, Tuple
import requests
from bs4 import BeautifulSoup
from redminelib import Redmine
from redminelib.exceptions import ForbiddenError
from redminelib.resources.standard import Project, User
import utils as ut


def check_auth(func: Callable):
    """
    Decorator checks authentication of user to Redmine.
    :param func: decorated method.
    """

    def wrapper(self, *args):
        """
        :param self: object of class;
        :param args: arguments for method.
        """

        if self.user is None:
            print("User is not logged in to https://ximc.ru")
            return
        return func(self, *args)

    return wrapper


class XimcRedmine:
    """
    Class to work with ximc Redmine.
    """

    def __init__(self, username: str, password: str):
        """
        :param username: username in ximc Redmine;
        :param password: password to ximc Redmine.
        """

        self._all_projects = None
        self._filters: list = []
        self._password: str = password
        self._projects: list = []
        self._redmine: Redmine = Redmine("https://ximc.ru", username=username, password=password)
        self._totals_options: dict = {}
        self._username: str = username
        self.user: User = None

    def _find_project_id(self, project_name: str) -> Optional[str]:
        """
        Method searches identifier of project with given name.
        :param project_name: project name.
        :return: project identifier.
        """

        projects = self._redmine.project.all()
        if isinstance(projects, Iterable):
            for project in projects:
                if project.name == project_name:
                    return project.id
        return None

    def _get_user_id(self, username: str) -> Optional[int]:
        """
        Method returns ID of user who works in given project.
        :param username: username.
        :return: user ID.
        """

        def get_user_from_memberships(memberships) -> Optional[int]:
            for membership in memberships:
                user = getattr(membership, "user", None)
                if user is not None and user.name == username:
                    return user.id
            return None

        if self._projects:
            for project_id, _ in self._projects:
                memberships = self._redmine.project_membership.filter(project_id=project_id)
                user_id = get_user_from_memberships(memberships)
                if user_id is not None:
                    return user_id
        for project in self._all_projects:
            user_id = get_user_from_memberships(project.memberships)
            if user_id is not None:
                return user_id
        return None

    def _get_version_id(self, version_name: str) -> Optional[int]:
        """
        Method returns ID of version for given project.
        :param version_name: name of project version.
        :return: version ID.
        """

        if self._projects:
            for project_id, _ in self._projects:
                versions = self._redmine.version.filter(project_id=project_id)
                for version in versions:
                    if version.name == version_name:
                        return version.id
        for project in self._all_projects:
            versions = self._redmine.version.filter(project_id=project.id)
            for version in versions:
                if version.name == version_name:
                    return version.id
        return None

    def _parse_info_from_issues_page(self, url: str):
        """
        Method parses information from page with issues.
        :param url: url address of page with filtered issues.
        """

        try:
            html = requests.get(url, auth=(self._username, self._password), timeout=3).text
        except requests.exceptions:
            return {}
        soup = BeautifulSoup(html, "html.parser")
        ps_query_totals = soup.find_all("p", {"class": "query-totals"})
        for p_query_totals in ps_query_totals:
            for span in p_query_totals.find_all("span", {"class": re.compile("total-for-")}):
                for total_option in self._totals_options:
                    real_option_name = ut.TOTALS_OPTIONS[total_option.lower()].replace("_", "-")
                    if span["class"][0] == f"total-for-{real_option_name}":
                        value_span = span.find("span", {"class": "value"})
                        self._totals_options[total_option] = float(value_span.get_text())

    @check_auth
    def add_filter(self, filter_name: str, operator_name: str, *values):
        """
        Method adds new filter.
        :param filter_name: name of filter;
        :param operator_name: name of operator for filter;
        :param values: values for filter.
        """

        filter_name = filter_name.lower()
        operator_name = operator_name.lower()
        if len(values) == 0:
            value = None
        elif operator_name in ("между", "between"):
            value = values[0]
            value_2 = values[1]
        else:
            value = values[0]
        real_filter_name, value = ut.find_real_filter_name_and_value(filter_name, value)
        if value is not None and real_filter_name in ut.FILTERS_WITH_USERS:
            value = self._get_user_id(value)
        elif filter_name in ("версия", "target version"):
            value = self._get_version_id(value)
        elif filter_name in ("проект", "project"):
            project_id = self._find_project_id(value)
            self._projects.append((project_id, value))
            value = project_id
        operator = ut.find_operator(operator_name)
        for filter_obj in self._filters:
            if (value is None and real_filter_name == filter_obj.get("filter") and
                    operator == filter_obj.get("operator")):
                values = filter_obj.get("values")
                if value not in values:
                    filter_obj["values"].append(value)
                return
        self._filters.append({"filter": real_filter_name,
                              "operator": operator,
                              "values": [] if value is None else [value]})
        if operator_name in ("между", "between"):
            self._filters[-1]["values"].append(value_2)

    def auth(self):
        """
        Method authenticates user in Redmine.
        """

        self.user = self._redmine.auth()
        self._all_projects = self._redmine.project.all()

    def clear_filters(self):
        """
        Method clears filters.
        """

        self._filters = []
        self._projects = []

    def get_filters(self) -> list:
        """
        Method returns list with filters.
        :return: list with filters.
        """

        return self._filters

    @check_auth
    def get_groups(self):
        """
        Method returns groups. To work with groups in Redmine user must have special
        permission.
        :return: groups.
        """

        groups = self._redmine.group.all()
        try:
            for _ in groups:
                pass
        except ForbiddenError:
            print("You do not have permission to work with groups")
            raise
        return groups

    @check_auth
    def get_project(self, project_name: str) -> Optional[Project]:
        """
        Method returns project with given name.
        :param project_name: name of project.
        :return: project.
        """

        for project in self._all_projects:
            if project.name == project_name:
                try:
                    project = self._redmine.project.get(project.id)
                    return project
                except Exception:
                    return None
        return None

    @check_auth
    def get_projects(self) -> List[Tuple[int, str]]:
        """
        Method returns IDs and names of all available projects.
        :return: IDs and names of available projects.
        """

        return [(project.id, project.name) for project in self._redmine.project.all()]

    @check_auth
    def get_roles(self) -> List[Tuple[int, str]]:
        """
        Method returns roles for Redmine users.
        :return: list with IDs and names of roles.
        """

        return [(role.id, role.name) for role in self._redmine.role.all()]

    @check_auth
    def get_totals(self, *totals_options) -> Dict[str, Optional[float]]:
        """
        Method returns values for given totals options for project issues.
        :param totals_options: list with required totals options.
        :return: dictionary with values of required options.
        """

        self._totals_options = {}
        for option in totals_options:
            if option.lower() in ut.TOTALS_OPTIONS:
                self._totals_options[option] = None
        url = ut.create_url(self._filters, self._totals_options)
        self._parse_info_from_issues_page(url)
        return self._totals_options

    @check_auth
    def get_users(self):
        """
        Method returns users. To work with users in Redmine user must have special
        permission.
        :return: users.
        """

        users = self._redmine.user.all()
        try:
            for _ in users:
                pass
        except ForbiddenError:
            print("You do not have permission to work with users")
            raise
        return users

    @check_auth
    def get_versions_for_project(self, project_name: str) -> List[Tuple[int, str]]:
        """
        Method returns versions for project with given name.
        :param project_name: name of project for which all versions should be returned.
        :return: IDs and names of versions for given project.
        """

        project_identifier = self._find_project_id(project_name)
        versions = self._redmine.version.filter(project_id=project_identifier)
        return [(version.id, version.name) for version in versions]
