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

    # Задаем параметры для первого запроса
    # Задаем имя проекта
    ximc_user.set_project("EP-software")
    # Задаем фильтры аналогично веб-интерфейсу ximc
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
    totals = ximc_user.get_totals("Оценка временных затрат", "Трудозатраты", "Payment cash",
                                  "Payment cashless", "Rate")
    # В итоге получаем словарь в виде: {"название параметра": значение}
    print("Project: EP-software")
    for option_name, value in totals.items():
        print(f"{option_name}: {value}")

    # Задаем параметры для следующего запроса
    # ОБЯЗАТЕЛЬНО задаем имя проекта (даже если проект тот же)
    ximc_user.set_project("Payments")
    # Задаем фильтры аналогично веб-интерфейсу ximc
    ximc_user.add_filter("Статус", "закрыто")
    ximc_user.add_filter("Создано", "между", "2021-09-09", "2021-11-11")
    # Запрашиваем необходимые итоговые параметры
    totals = ximc_user.get_totals("Оценка временных затрат", "Трудозатраты", "Payment cash",
                                  "Payment cashless", "Rate", "Payment tail")
    # В итоге получаем словарь в виде: {"название параметра": значение}
    print("\nProject: Payments")
    for option_name, value in totals.items():
        print(f"{option_name}: {value}")
