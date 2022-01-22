import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

import fetch_hh
import fetch_sj


if __name__ == '__main__':
    load_dotenv()

    hh_api_url = 'https://api.hh.ru/vacancies'

    hh_speciality = 'программист'

    sj_api_url = 'https://api.superjob.ru/2.0/vacancies/'

    sj_headers = {
        'X-Api-App-Id': os.getenv('SJ_API_KEY')
    }

    pop_languages = os.getenv('POP_LANGUAGES').split(",")

    table_heading = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    hh_table = []
    sj_table = []

    for language in pop_languages:
        found_hh_vacancies = fetch_hh.fetch_hh_vacancies_info(hh_api_url, hh_speciality, 1, 30, language)
        found_sj_vacancies = fetch_sj.fetch_sj_vacancies_info(sj_api_url, sj_headers, language)

        vacancies_hh_processed = 0
        vacancies_sj_processed = 0

        hh_salary_sum = 0
        sj_salary_sum = 0

        for vacancy in found_hh_vacancies[0]:
            vacancy_salary = fetch_hh.predict_rub_salary(vacancy)
            if vacancy_salary:
                hh_salary_sum += int(vacancy_salary)
                vacancies_hh_processed += 1

        for vacancy in found_sj_vacancies[0]:
            vacancy_salary = fetch_sj.predict_rub_salary_for_superJob(vacancy)
            if vacancy_salary:
                sj_salary_sum += int(vacancy_salary)
                vacancies_sj_processed += 1

        hh_table += [[language,
                      found_hh_vacancies[1],
                      vacancies_hh_processed,
                      int(hh_salary_sum / vacancies_hh_processed)
                      ]]

        sj_table += [[language,
                      found_sj_vacancies[1],
                      vacancies_sj_processed,
                      int(sj_salary_sum / vacancies_sj_processed)
                      ]]

    output_hh_table = AsciiTable(table_heading + hh_table, 'HeadHunter Moscow')
    output_sj_table = AsciiTable(table_heading + sj_table, 'SuperJob Moscow')

    print(f"""{output_hh_table.table}\n\n{output_sj_table.table}""")


