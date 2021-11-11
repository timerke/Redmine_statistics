"""
File with class to work with Ximc Redmine.
"""

import re
from typing import Callable, Dict, Iterable, List, Optional, Union
import requests
from bs4 import BeautifulSoup
from redminelib import Redmine
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

        self._filters: list = []
        self._password: str = password
        self._project_identifier: str = None
        self._redmine: Redmine = Redmine("https://ximc.ru", username=username, password=password)
        self._totals_options: dict = {}
        self._username: str = username
        self.user: User = None

    def _find_project_identifier(self, project_name: str) -> Optional[str]:
        """
        Method searches identifier of project with given name.
        :param project_name: project name.
        :return: project identifier.
        """

        projects = self._redmine.project.all()
        if isinstance(projects, Iterable):
            for project in projects:
                if project.name == project_name:
                    return project.identifier
        return None

    def _get_user_id(self, username: str) -> Optional[int]:
        """
        Method returns ID of user who works in given project.
        :param username: username.
        :return: user ID.
        """

        if self._project_identifier is None:
            raise RuntimeError("You need to specify the name of the project")
        memberships = self._redmine.project_membership.filter(project_id=self._project_identifier)
        for membership in memberships:
            user = getattr(membership, "user", None)
            if user is not None and user.name == username:
                return user.id
        return None

    def _get_version_id(self, version_name: str) -> Optional[int]:
        """
        Method returns ID of version for given project.
        :param version_name: name of project version.
        :return: version ID.
        """

        versions = self._redmine.version.filter(project_id=self._project_identifier)
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
                    real_option_name = ut.TOTALS_OPTIONS[total_option].replace("_", "-")
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

        if len(values) == 0:
            value = None
        elif operator_name != "между":
            value = values[0]
        else:
            value = values[0]
            value_2 = values[1]
        real_filter_name, value = ut.find_real_filter_name_and_value(filter_name, value)
        if value is not None and filter_name in ut.FILTERS_WITH_USERS:
            value = self._get_user_id(value)
        elif filter_name == "Версия":
            value = self._get_version_id(value)
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
        if operator_name == "между":
            self._filters[-1]["values"].append(value_2)

    def auth(self):
        """
        Method authenticates user in Redmine.
        """

        self.user = self._redmine.auth()

    def clear_filters(self):
        """
        Method clears filters.
        """

        self._filters = []

    def get_filters(self) -> list:
        """
        Method returns list with filters.
        :return: list with filters.
        """

        return self._filters

    @check_auth
    def get_project(self, project_name: str) -> Optional[Project]:
        """
        Method returns project with given name.
        :param project_name: name of project.
        :return: project.
        """

        for project in self._redmine.project.all():
            if project.name == project_name:
                try:
                    project = self._redmine.project.get(project.id)
                    return project
                except Exception:
                    return None
        return None

    @check_auth
    def get_projects_names(self) -> List[str]:
        """
        Method returns names of all available projects.
        :return: names of available projects.
        """

        for project in self._redmine.project.all():
            yield project.name

    @check_auth
    def get_totals(self, *totals_options) -> Dict[str, Optional[float]]:
        """
        Method returns values for given totals options for project issues.
        :param totals_options: list with required totals options.
        :return: dictionary with values of required options.
        """

        self._totals_options = {}
        for option in totals_options:
            if option in ut.TOTALS_OPTIONS:
                self._totals_options[option] = None
        url = ut.create_url(self._project_identifier, self._filters, self._totals_options)
        self._parse_info_from_issues_page(url)
        return self._totals_options

    @check_auth
    def set_project(self, project_name: str):
        """
        Method sets project for which totals will be calculated.
        :param project_name: project name.
        """

        self._project_identifier = self._find_project_identifier(project_name)
        self.clear_filters()
