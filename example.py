"""
Example file.
"""

import sys
from ximc import XimcRedmine

if __name__ == "__main__":

    user_name = ""
    password = ""
    try:
        ximc_user = XimcRedmine(user_name, password)
        ximc_user.auth()
    except Exception:
        print("User authorization failed")
        sys.exit(0)

    # Задаем параметры для первого запроса (фильтры задаются аналогично веб-интерфейсу ximc)
    ximc_user.add_filter("Проект", "соответствует", "EP-software")
    ximc_user.add_filter("Статус", "соответствует", "Closed")
    ximc_user.add_filter("Трекер", "не соответствует", "Bug")
    ximc_user.add_filter("Приоритет", "соответствует", "Normal")
    ximc_user.add_filter("Автор", "не соответствует", "dasha")
    ximc_user.add_filter("Назначена", "все")
    ximc_user.add_filter("Версия", "соответствует", "Развитие-2018")
    ximc_user.add_filter("Тема", "содержит", "к нашим")
    ximc_user.add_filter("Описание", "начинается с", "Привести")
    ximc_user.add_filter("Готовность", ">=", 50)
    ximc_user.add_filter("Частная", "соответствует", "нет")
    ximc_user.add_filter("Файл", "отсутствует")
    ximc_user.add_filter("Кем изменено", "соответствует", "mikheev")
    ximc_user.add_filter("Последний изменивший", "соответствует", "VladBelov")
    ximc_user.add_filter("Задача", ">=", 20033)
    # Запрашиваем необходимые итоговые параметры
    totals = ximc_user.get_totals("Оценка временных затрат", "Трудозатраты", "Payment cash", "Payment cashless", "Rate")
    # В итоге получаем словарь в виде: {"название параметра": значение}
    print("Project: EP-software")
    for option_name, value in totals.items():
        print(f"{option_name}: {value}")

    # Задаем параметры для следующего запроса. Но сначала нужно очистить ранее заданные фильтры
    ximc_user.clear_filters()
    # Задаем фильтры аналогично веб-интерфейсу ximc
    ximc_user.add_filter("Project", "is", "Payments")
    ximc_user.add_filter("Status", "closed")
    ximc_user.add_filter("Created", "between", "2021-09-09", "2021-11-11")
    # Запрашиваем необходимые итоговые параметры
    totals = ximc_user.get_totals("Estimated time", "Spent time", "Payment cash", "Payment cashless", "Rate",
                                  "Payment tail")
    # В итоге получаем словарь в виде: {"название параметра": значение}
    print("\nProject: Payments")
    for option_name, value in totals.items():
        print(f"{option_name}: {value}")

    # Задаем параметры для следующего запроса. Но сначала нужно очистить ранее заданные фильтры
    ximc_user.clear_filters()
    ximc_user.add_filter("Status", "is", "Closed")
    ximc_user.add_filter("Tracker", "is not", "Bug")
    ximc_user.add_filter("Priority", "is", "Normal")
    ximc_user.add_filter("Author", "is", "dasha")
    ximc_user.add_filter("Assignee", "is", "vladimirov_iy")
    ximc_user.add_filter("% Done", ">=", 50)
    # Запрашиваем необходимые итоговые параметры
    totals = ximc_user.get_totals("Estimated time", "Spent time", "Payment cash", "Payment cashless", "Rate")
    # В итоге получаем словарь в виде: {"название параметра": значение}
    print("\nAll projects")
    for option_name, value in totals.items():
        print(f"{option_name}: {value}")
