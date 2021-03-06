import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

import fetch_hh
import fetch_sj


def predict_rub_salary(salary_currency, salary_from, salary_to):
    if salary_currency not in ["RUR", 'rub']:
        return None

    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    else:
        return (salary_from or 0) * 1.2 + (salary_to or 0) * 0.8


def make_hh_table(vacancies, language):
    results_table = []
    vacancies_hh_processed = 0
    hh_salary_sum = 0

    for vacancy in vacancies[0]:
        if not vacancy['salary']:
            continue

        vacancy_salary = predict_rub_salary(vacancy['salary']['currency'],
                                            vacancy['salary']['from'],
                                            vacancy['salary']['to'])

        if not vacancy_salary:
            continue

        hh_salary_sum += int(vacancy_salary)
        vacancies_hh_processed += 1

    results_table += [[language,
                  vacancies[1],
                  vacancies_hh_processed,
                  int(hh_salary_sum / (vacancies_hh_processed or 1))
                  ]]

    return results_table


def make_sj_table(vacancies, language):
    results_table = []
    vacancies_sj_processed = 0
    sj_salary_sum = 0

    for vacancy in vacancies[0]:
        if not vacancy["payment_from"] and not vacancy["payment_to"]:
            continue

        vacancy_salary = predict_rub_salary(vacancy["currency"],
                                            vacancy["payment_from"],
                                            vacancy["payment_to"])

        if not vacancy_salary:
            continue

        sj_salary_sum += int(vacancy_salary)
        vacancies_sj_processed += 1

    results_table += [[language,
                  vacancies[1],
                  vacancies_sj_processed,
                  int(sj_salary_sum / (vacancies_sj_processed or 1))
                  ]]

    return results_table


if __name__ == '__main__':
    load_dotenv()

    hh_speciality = '??????????????????????'

    sj_headers = {
        'X-Api-App-Id': os.getenv('SJ_API_KEY')
    }

    pop_languages = os.getenv('POP_LANGUAGES').split(",")

    table_heading = [['???????? ????????????????????????????????', '???????????????? ??????????????', '???????????????? ????????????????????', '?????????????? ????????????????']]

    hh_table = []
    sj_table = []

    hh_search_city = 1  # City`s id. 1 - Moscow
    hh_search_period = 30

    for language in pop_languages:
        found_hh_vacancies = fetch_hh.fetch_hh_vacancies_info(hh_speciality, hh_search_city, hh_search_period, language)
        found_sj_vacancies = fetch_sj.fetch_sj_vacancies_info(sj_headers, language)

        hh_table += make_hh_table(found_hh_vacancies, language)
        sj_table += make_sj_table(found_sj_vacancies, language)

    output_hh_table = AsciiTable(table_heading + hh_table, 'HeadHunter Moscow')
    output_sj_table = AsciiTable(table_heading + sj_table, 'SuperJob Moscow')

    print(f"""{output_hh_table.table}\n\n{output_sj_table.table}""")
