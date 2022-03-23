import configparser
import json
import sys
from datetime import datetime
from ximc import XimcRedmine

# Курс валюты, необходим для сведения финальных рублевых цифр
USD_CB = 75.1
# Интервалы, в которые будет собираться статистика
QUARTERS = {"Q1 2018": ("2018-01-01", "2018-03-31"),
            "Q2 2018": ("2018-04-01", "2018-06-30"),
            "Q3 2018": ("2018-07-01", "2018-09-30"),
            "Q4 2018": ("2018-10-01", "2018-12-31"),
            "Q1 2019": ("2019-01-01", "2019-03-31"),
            "Q2 2019": ("2019-04-01", "2019-06-30"),
            "Q3 2019": ("2019-07-01", "2019-09-30"),
            "Q4 2019": ("2019-10-01", "2019-12-31"),
            "Q1 2020": ("2020-01-01", "2020-03-31"),
            "Q2 2020": ("2020-04-01", "2020-06-30"),
            "Q3 2020": ("2020-07-01", "2020-09-30"),
            "Q4 2020": ("2020-10-01", "2020-12-31"),
            "Q1 2021": ("2021-01-01", "2021-03-31"),
            "Q2 2021": ("2021-04-01", "2021-06-30"),
            "Q3 2021": ("2021-07-01", "2021-09-30"),
            "Q4 2021": ("2021-10-01", "2021-12-31")}

# Проекты, с которыми будем работать, делим их на 4 группы: Malt, EZ, Raw, Zap.
# Причем группа Raw содержит только платежи, но не сожержит связанных с ними проектов
MALT_PROJ_LIST = ["ADC", "Buk2-Burg2", "DAC", "DPLL", "Freon", "Magma", "NPU", "Open", "PIC", "Shared", "MALT2011-20"]
MALT_PAYMENT_LIST = ["ADC-payments", "Burg2-payments", "DAC-payments", "DPLL-payments", "Freon-payments",
                     "Magma-payments", "NPU-payments", "Open-payments", "PIC-payments", "Shared-payments",
                     "allpayments"]
EZ_PROJ_LIST = ["AI", "Bombardie", "Dauria", "EyePoint", "Fazli", "General", "Meridian", "Printeltech", "RAC", "TP",
                "TVI", "UltraRay", "XBB", "ximc"]
EZ_PAYMENT_LIST = ["EN-Payments", "Bom-Payments", "DA-Payments", "EP-Payments", "FAZ-Payments", "Gen-Payments",
                   "M-Payments", "PET-Payments", "RAC-Payments", "TP-Payments", "TVI-Payments", "UR-Payments",
                   "XBB-Payments", "XI-Payments"]
RAW_PAYMENT_LIST = ["Dividends", "Payments"]
ZAP_PROJ_LIST = ["Z30", "ZEL", "ZRocket"]
ZAP_PAYMENT_LIST = ["Z30-Payments", "ZEL-Payments", "ZRocket"]


def save_results_to_json_file(file_name: str, data: dict):
    """
    Function saves results to JSON-files.
    :param file_name: name of file to save data.
    :param data: data to save.
    """

    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file)


def get_incomes_or_expenditures(ximc_user: XimcRedmine, rub: bool, income: bool, project_name: str, start_date: str,
                                stop_date: str) -> float:
    """
    Function returns RUB or USD income or expenditure for given period.
    :param ximc_user: authorized to Redmine user;
    :param rub: if True then RUB will be used otherwise USD;
    :param income: if True then income will be returned otherwise expenditure;
    :param project_name: name of project;
    :param start_date: quarter start date;
    :param stop_date: quarter end date.
    :return: RUB or USD income or expenditure.
    """

    # Задаем фильтры
    ximc_user.clear_filters()
    ximc_user.add_filter("Проект", "соответствует", project_name)
    ximc_user.add_filter("Статус", "соответствует", "Closed")
    ximc_user.add_filter("Трекер", "соответствует", "Payment")
    ximc_user.add_filter("Срок завершения", "между", start_date, stop_date)
    if rub:
        ximc_user.add_filter("Тема", "не содержит", "валют")
    else:
        ximc_user.add_filter("Тема", "содержит", "валют")
    if income:
        ximc_user.add_filter("Payment category", "соответствует", "Income")
    else:
        ximc_user.add_filter("Payment category", "не соответствует", "Income")
    # Запрашиваем необходимые итоговые параметры
    total = 0
    totals = ximc_user.get_totals("Payment cash", "Payment cashless")
    if totals["Payment cash"] is not None:
        total += totals["Payment cash"]
    if totals["Payment cashless"] is not None:
        total += totals["Payment cashless"]
    return total


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    user_name = config.get("MAIN", "login")
    password = config.get("MAIN", "password")
    try:
        ximc_user = XimcRedmine(user_name, password)
        ximc_user.auth()
    except Exception:
        print("User authorization failed")
        sys.exit(0)

    result = {}
    # Общий перечень проектов, включающий все, по нему можно общие сверять цифры с треккером
    print("\nОбщие доходы/расходы по всем проектам за 2018-2021 по кварталам:")
    payment_list = MALT_PAYMENT_LIST + EZ_PAYMENT_LIST + RAW_PAYMENT_LIST + ZAP_PAYMENT_LIST
    for project_name in payment_list:
        result[project_name] = {}
        print(project_name)
        for quarter_name, quarter_period in QUARTERS.items():
            start_date, stop_date = quarter_period
            income_rub = get_incomes_or_expenditures(ximc_user, True, True, project_name, start_date, stop_date)
            expenditure_rub = get_incomes_or_expenditures(ximc_user, True, False, project_name, start_date, stop_date)
            income_usd = get_incomes_or_expenditures(ximc_user, False, True, project_name, start_date, stop_date)
            expenditure_usd = get_incomes_or_expenditures(ximc_user, False, False, project_name, start_date, stop_date)
            print(f"{quarter_name} ({quarter_period[0]} - {quarter_period[1]}):", income_rub, expenditure_rub,
                  income_usd, expenditure_usd)
            result[project_name][quarter_name] = {"INCOME_RUB": income_rub,
                                                  "EXPENDITURE_RUB": expenditure_rub,
                                                  "INCOME_USD": income_usd,
                                                  "EXPENDITURE_USD": expenditure_usd}
    # Сохраняем данные
    file_name = f"finances {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.json"
    save_results_to_json_file(file_name, result)
    print(f"Результаты сохранены в файл '{file_name}'")
