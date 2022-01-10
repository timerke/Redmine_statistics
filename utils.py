"""
File with useful functions and constants.
"""

from typing import Optional, Tuple

BRACKET_CONVERTER = {"[": "%5B",
                     "]": "%5D"}

OPERATOR_LABELS = {"=": ("соответствует", "is"),
                   "!": ("не соответствует", "is not"),
                   "o": ("открыто", "open"),
                   "c": ("закрыто", "closed"),
                   "!*": ("отсутствует", "none"),
                   "*": ("все", "any"),
                   ">=": (">=",),
                   "<=": ("<=",),
                   "><": ("между", "between"),
                   "<t+": ("менее чем", "is less than"),
                   ">t+": ("более чем", "is more than"),
                   "><t+": ("в следующие дни", "in the next"),
                   "t+": ("в", "in"),
                   "nd": ("завтра", "tomorrow"),
                   "t": ("сегодня", "today"),
                   "ld": ("вчера", "yesterday"),
                   "nw": ("следующая неделя", "next week"),
                   "w": ("на этой неделе", "this week"),
                   "lw": ("прошлая неделя", "last week"),
                   "l2w": ("прошлые 2 недели", "last 2 weeks"),
                   "nm": ("следующий месяц", "next month"),
                   "m": ("этот месяц", "this month"),
                   "lm": ("прошлый месяц", "last month"),
                   "y": ("этот год", "this year"),
                   ">t-": ("менее, чем дней(я) назад", "less than days ago"),
                   "<t-": ("более, чем дней(я) назад", "more than days ago"),
                   "><t-": ("в прошлые дни", "in the past"),
                   "t-": ("дней(я) назад", "days ago"),
                   "~": ("содержит", "contains"),
                   "!~": ("не содержит", "doesn't contain"),
                   "^": ("начинается с", "starts with"),
                   "$": ("заканчивается на", "ends with"),
                   "=p": ("любые задачи в проекте", "any issues in project"),
                   "=!p": ("любые задачи не в проекте", "any issues not in project"),
                   "!p": ("нет задач в проекте", "no issues in project"),
                   "*o": ("любые открытые задачи", "any open issues"),
                   "!o": ("нет открытых задач", "no open issues")}

SYMBOLS_DECODING = {"=": "%3D",
                    "!": "%21",
                    "+": "%2B",
                    " ": "+"}

OPERATOR_BY_TYPES = {"list": ["=", "!"],
                     "list_status": ["o", "=", "!", "c", "*"],
                     "list_optional": ["=", "!", "!*", "*"],
                     "list_subprojects": ["*", "!*", "=", "!"],
                     "date": ["=", ">=", "<=", "><", "<t+", ">t+", "><t+", "t+", "nd", "t", "ld", "nw", "w", "lw",
                              "l2w", "nm", "m", "lm", "y", ">t-", "<t-", "><t-", "t-", "!*", "*"],
                     "date_past": ["=", ">=", "<=", "><", ">t-", "<t-", "><t-", "t-", "t", "ld", "w", "lw", "l2w",
                                   "m", "lm", "y", "!*", "*"],
                     "string": ["~", "=", "!~", "!", "^", "$", "!*", "*"],
                     "text": ["~", "!~", "^", "$", "!*", "*"],
                     "integer": ["=", ">=", "<=", "><", "!*", "*"],
                     "float": ["=", ">=", "<=", "><", "!*", "*"],
                     "relation": ["=", "!", "=p", "=!p", "!p", "*o", "!o", "!*", "*"],
                     "tree": ["=", "~", "!*", "*"]}

AVAILABLE_FILTERS = {
    "status_id": {"type": "list", "name": ("статус", "status"),
                  "values": [[("new",), "1"], [("assigned",), "2"], [("resolved",), "3"], [("feedback",), "4"],
                             [("closed",), "5"], [("rejected",), "6"]]},
    "project_id": {"type": "list", "name": ("проект", "project")},
    "tracker_id": {"type": "list", "name": ("трекер", "tracker"),
                   "values": [[("bug",), "1"], [("feature",), "2"], [("support",), "3"], [("payment",), "4"]]},
    "priority_id": {"type": "list", "name": ("приоритет", "priority"),
                    "values": [[("background",), "12"], [("low",), "3"], [("normal",), "4"], [("high",), "5"],
                               [("urgent",), "6"], [("immediate",), "7"]]},
    "author_id": {"type": "list", "name": ("автор", "author")},
    "assigned_to_id": {"type": "list", "name": ("назначена", "assignee")},
    "member_of_group": {"type": "list", "name": ("группа назначенного", "assignee's group")},
    "assigned_to_role": {"type": "list", "name": ("роль назначенного", "assignee's role")},
    "fixed_version_id": {"type": "list_optional", "name": ("версия", "target version")},
    "fixed_version.due_date": {"type": "date", "name": ("версия дата", "target version's due date")},
    "fixed_version.status": {"type": "list", "name": ("версия статус", "target version's status"),
                             "values": [[("открыт", "open"), "open"], [("заблокирован", "locked"), "locked"],
                                        [("закрыт", "closed"), "closed"]]},
    "fixed_version.cf_32": {"type": "list", "name": ("версия supervisor", "target version's supervisor")},
    "fixed_version.cf_36": {"type": "list", "name": ("версия mature", "target version's mature"),
                            "values": [[("да", "yes"), "1"], [("нет", "no"), "0"]]},
    "subject": {"type": "text", "name": ("тема", "subject")},
    "description": {"type": "text", "name": ("описание", "description")},
    "created_on": {"type": "date", "name": ("создано", "created")},
    "updated_on": {"type": "date", "name": ("обновлено", "updated")},
    "closed_on": {"type": "date_past", "name": ("закрыта", "closed")},
    "start_date": {"type": "date", "name": ("дата начала", "start date")},
    "due_date": {"type": "date", "name": ("срок завершения", "due date")},
    "estimated_hours": {"type": "float", "name": ("оценка временных затрат", "estimated time")},
    "spent_time": {"type": "float", "name": ("трудозатраты", "spent time")},
    "done_ratio": {"type": "integer", "name": ("готовность", "% done")},
    "is_private": {"type": "list", "name": ("частная", "private"),
                   "values": [[("да", "yes"), "1"], [("нет", "no"), "0"]]},
    "attachment": {"type": "text", "name": ("файл", "file")},
    "updated_by": {"type": "list", "name": ("кем изменено", "updated by")},
    "last_updated_by": {"type": "list", "name": ("последний изменивший", "last updated by")},
    "project.status": {"type": "list", "name": ("проект статус", "project's status")},
    "cf_28": {"type": "list_optional", "name": ("payment category",)},
    "cf_29": {"type": "integer", "name": ("payment cash",)},
    "cf_30": {"type": "integer", "name": ("payment cashless",)},
    "cf_38": {"type": "integer", "name": ("rate",)},
    "cf_39": {"type": "integer", "name": ("payment tail",)},
    "cf_41": {"type": "list", "name": ("company",)},
    "cf_42": {"type": "list", "name": ("валюта",)},
    "relates": {"type": "relation", "name": ("связана с", "related to")},
    "duplicates": {"type": "relation", "name": ("дублирует", "is duplicate of")},
    "duplicated": {"type": "relation", "name": ("дублируется", "has duplicate")},
    "blocks": {"type": "relation", "name": ("блокирует", "blocks")},
    "blocked": {"type": "relation", "name": ("блокируется", "blocked by")},
    "precedes": {"type": "relation", "name": ("следующая", "precedes")},
    "follows": {"type": "relation", "name": ("предыдущая", "follows")},
    "copied_to": {"type": "relation", "name": ("скопирована в", "copied to")},
    "copied_from": {"type": "relation", "name": ("скопирована с", "copied from")},
    "start_to_start": {"type": "relation", "name": ("старт --> старт", "start to start")},
    "finish_to_finish": {"type": "relation", "name": ("финиш --> финиш", "finish to finish")},
    "start_to_finish": {"type": "relation", "name": ("начало-окончание", "start to finish")},
    "parent_id": {"type": "tree", "name": ("родительская задача", "parent task")},
    "child_id": {"type": "tree", "name": ("подзадачи", "subtasks")},
    "issue_id": {"type": "integer", "name": ("задача", "issue")},
    "last_spent_on": {"type": "date", "name": ("последняя запись времени", "last spent time")},
    "watcher_id": {"type": "list", "name": ("наблюдатель", "watcher")},
    "issue_tags": {"type": "text", "name": ("метки", "tags")}}

FILTERS_WITH_USERS = ("author_id", "assigned_to_id", "updated_by", "last_updated_by", "watcher_id")

TOTALS_OPTIONS = {"оценка временных затрат": "estimated_hours",
                  "estimated time": "estimated_hours",
                  "трудозатраты": "spent_hours",
                  "spent time": "spent_hours",
                  "payment cash": "cf_29",
                  "payment cashless": "cf_30",
                  "rate": "cf_38",
                  "payment tail": "cf_39"}


def create_url(filters: list, totals_options: dict) -> str:
    """
    Function creates url address to get required data from ximc.
    :param filters: filters for required data;
    :param totals_options: list of required options.
    :return: url address.
    """

    url = f"https://ximc.ru/issues?utf8=✓&set_filter=1&sort=id%3Adesc"
    # Part with filters
    for filter_obj in filters:
        filter_name = filter_obj.get("filter")
        filter_operator = filter_obj.get("operator")
        filter_values = filter_obj.get("values")
        if filter_name is not None:
            url += f"&f%5B%5D={filter_name}"
            decoded_filter_operator = decode_symbols(filter_operator)
            url += f"&op%5B{filter_name}%5D={decoded_filter_operator}"
            for filter_value in filter_values:
                if filter_operator in ("~", "!~", "^", "$"):
                    value = decode_symbols(filter_value)
                else:
                    value = filter_value
                url += f"&v%5B{filter_name}%5D%5B%5D={value}"
    # Part with totals
    for option in totals_options:
        real_option_name = TOTALS_OPTIONS[option.lower()]
        url += f"&t%5B%5D={real_option_name}"
    return url


def decode_symbols(word: str) -> str:
    """
    Function decodes string.
    :param word: string to decode.
    :return: decoded string.
    """

    decoded_word = ""
    for symbol in word:
        decoded_word += SYMBOLS_DECODING.get(symbol, symbol)
    return decoded_word


def find_operator(operator_name: str) -> Optional[str]:
    """
    Function finds real name (identifier) for operator with given user friendly
    name.
    :param operator_name: use friendly name of operator.
    :return: real name of operator.
    """

    for real_name, friendly_name in OPERATOR_LABELS.items():
        if operator_name in friendly_name:
            return real_name
    return None


def find_real_filter_name_and_value(filter_name: str, value: Optional[str] = None) -> Optional[Tuple[str, str]]:
    """
    Function finds real name (identifier) for filter with given user friendly name.
    :param filter_name: user friendly name of filter;
    :param value: value of filter.
    :return: real name of filter.
    """

    for real_name, available_filter in AVAILABLE_FILTERS.items():
        if filter_name.lower() in available_filter["name"]:
            if value is not None:
                available_values = available_filter.get("values", [])
                for available_value, value_id in available_values:
                    if value.lower() in available_value:
                        value = value_id
                        break
            return real_name, value
    return None
