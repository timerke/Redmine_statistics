"""
File with useful functions and constants.
"""

from typing import Optional, Tuple

BRACKET_CONVERTER = {"[": "%5B",
                     "]": "%5D"}

OPERATOR_LABELS = {
    "=": "соответствует",
    "!": "не соответствует",
    "o": "открыто",
    "c": "закрыто",
    "!*": "отсутствует",
    "*": "все",
    ">=": ">=",
    "<=": "<=",
    "><": "между",
    "<t+": "менее чем",
    ">t+": "более чем",
    "><t+": "в следующие дни",
    "t+": "в",
    "nd": "завтра",
    "t": "сегодня",
    "ld": "вчера",
    "nw": "следующая неделя",
    "w": "на этой неделе",
    "lw": "прошлая неделя",
    "l2w": "прошлые 2 недели",
    "nm": "следующий месяц",
    "m": "этот месяц",
    "lm": "прошлый месяц",
    "y": "этот год",
    ">t-": "менее, чем дней(я) назад",
    "<t-": "более, чем дней(я) назад",
    "><t-": "в прошлые дни",
    "t-": "дней(я) назад",
    "~": "содержит",
    "!~": "не содержит",
    "^": "начинается с",
    "$": "заканчивается на",
    "=p": "любые задачи в проекте",
    "=!p": "любые задачи не в проекте",
    "!p": "нет задач в проекте",
    "*o": "любые открытые задачи",
    "!o": "нет открытых задач"}

SYMBOLS_DECODING = {
    "=": "%3D",
    "!": "%21",
    "+": "%2B",
    " ": "+"}

OPERATOR_BY_TYPES = {
    "list": ["=", "!"],
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
    "status_id": {
        "type": "list_status", "name": "Статус", "remote": True,
        "values": [["New", "1"], ["Assigned", "2"], ["Resolved", "3"], ["Feedback", "4"],
                   ["Closed", "5"], ["Rejected", "6"]]},
    "project_id": {"type": "list", "name": "Проект", "remote": True},
    "tracker_id": {
        "type": "list", "name": "Трекер",
        "values": [["Bug", "1"], ["Feature", "2"], ["Support", "3"], ["Payment", "4"]]},
    "priority_id": {
        "type": "list", "name": "Приоритет",
        "values": [["Background", "12"], ["Low", "3"], ["Normal", "4"], ["High", "5"],
                   ["Urgent", "6"], ["Immediate", "7"]]},
    "author_id": {"type": "list", "name": "Автор", "remote": True},
    "assigned_to_id": {"type": "list_optional", "name": "Назначена", "remote": True},
    "member_of_group": {"type": "list_optional", "name": "Группа назначенного", "remote": True},
    "assigned_to_role": {"type": "list_optional", "name": "Роль назначенного", "remote": True},
    "fixed_version_id": {"type": "list_optional", "name": "Версия", "remote": True},
    "fixed_version.due_date": {"type": "date", "name": "Версия Дата", "values": None},
    "fixed_version.status": {
        "type": "list", "name": "Версия Статус",
        "values": [["открыт", "open"], ["заблокирован", "locked"], ["закрыт", "closed"]]},
    "subject": {"type": "text", "name": "Тема", "values": None},
    "description": {"type": "text", "name": "Описание", "values": None},
    "created_on": {"type": "date_past", "name": "Создано", "values": None},
    "updated_on": {"type": "date_past", "name": "Обновлено", "values": None},
    "closed_on": {"type": "date_past", "name": "Закрыта", "values": None},
    "start_date": {"type": "date", "name": "Дата начала", "values": None},
    "due_date": {"type": "date", "name": "Срок завершения", "values": None},
    "estimated_hours": {"type": "float", "name": "Оценка временных затрат", "values": None},
    "spent_time": {"type": "float", "name": "Трудозатраты", "values": None},
    "done_ratio": {"type": "integer", "name": "Готовность", "values": None},
    "is_private": {
        "type": "list", "name": "Частная", "values": [["да", "1"], ["нет", "0"]]},
    "attachment": {"type": "text", "name": "Файл", "values": None},
    "updated_by": {"type": "list", "name": "Кем изменено", "remote": True},
    "last_updated_by": {"type": "list", "name": "Последний изменивший", "remote": True},
    "project.status": {"type": "list", "name": "Проект Статус", "remote": True},
    "cf_28": {"type": "list_optional", "name": "Payment category", "remote": True},
    "cf_29": {"type": "integer", "name": "Payment cash", "values": None},
    "cf_30": {"type": "integer", "name": "Payment cashless", "values": None},
    "cf_38": {"type": "integer", "name": "Rate", "values": None},
    "cf_39": {"type": "integer", "name": "Payment tail", "values": None},
    "cf_41": {"type": "list_optional", "name": "Company", "remote": True},
    "cf_42": {"type": "list_optional", "name": "Валюта", "remote": True},
    "fixed_version.cf_32": {"type": "list_optional", "name": "Версия Supervisor", "remote": True},
    "fixed_version.cf_36": {"type": "list_optional", "name": "Версия Mature", "remote": True},
    "relates": {"type": "relation", "name": "связана с", "remote": True},
    "duplicates": {"type": "relation", "name": "дублирует", "remote": True},
    "duplicated": {"type": "relation", "name": "дублируется", "remote": True},
    "blocks": {"type": "relation", "name": "блокирует", "remote": True},
    "blocked": {"type": "relation", "name": "блокируется", "remote": True},
    "precedes": {"type": "relation", "name": "следующая", "remote": True},
    "follows": {"type": "relation", "name": "предыдущая", "remote": True},
    "copied_to": {"type": "relation", "name": "скопирована в", "remote": True},
    "copied_from": {"type": "relation", "name": "скопирована с", "remote": True},
    "start_to_start": {"type": "relation", "name": "Старт --> Старт", "remote": True},
    "finish_to_finish": {"type": "relation", "name": "Финиш --> Финиш", "remote": True},
    "start_to_finish": {"type": "relation", "name": "Начало-Окончание", "remote": True},
    "parent_id": {"type": "tree", "name": "Родительская задача", "values": None},
    "child_id": {"type": "tree", "name": "Подзадачи", "values": None},
    "issue_id": {"type": "integer", "name": "Задача", "values": None},
    "last_spent_on": {"type": "date_past", "name": "Последняя запись времени", "values": None},
    "watcher_id": {"type": "list", "name": "Наблюдатель", "values": []},
    "issue_tags": {"type": "issue_tags", "name": "Метки", "values": []}}

FILTERS_WITH_USERS = ("Автор", "Назначена", "Кем изменено", "Последний изменивший")

TOTALS_OPTIONS = {
    "Оценка временных затрат": "estimated_hours",
    "Трудозатраты": "spent_hours",
    "Payment cash": "cf_29",
    "Payment cashless": "cf_30",
    "Rate": "cf_38",
    "Payment tail": "cf_39"}


def create_url(project_identifier: str, filters: list, totals_options: dict) -> str:
    """
    Function creates url address to get required data from ximc.
    :param project_identifier: project identifier;
    :param filters: filters for required data;
    :param totals_options: list of required options.
    :return: url address.
    """

    url = f"https://ximc.ru/projects/{project_identifier}/issues?utf8=✓&set_filter=1&sort=id%3Adesc"
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
        real_option_name = TOTALS_OPTIONS[option]
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
        if friendly_name == operator_name:
            return real_name
    return None


def find_real_filter_name_and_value(filter_name: str, value: Optional[str] = None) ->\
        Optional[Tuple[str, str]]:
    """
    Function finds real name (identifier) for filter with given user friendly
    name.
    :param filter_name: user friendly name of filter;
    :param value: value of filter.
    :return: real name of filter.
    """

    for real_name, available_filter in AVAILABLE_FILTERS.items():
        if available_filter["name"] == filter_name:
            available_values = available_filter.get("values")
            if isinstance(available_values, (list, tuple)):
                for available_value, value_id in available_values:
                    if available_value == value:
                        value = value_id
                        break
            return real_name, value
    return None
