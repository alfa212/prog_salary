import requests


def fetch_hh_vacancies_info(text, area, period=0, lang=''):
    payload = {
        "text": text,
        "area": area,
        "per_page": 100
    }

    if period and period <= 30:
        payload["period"] = period

    if lang:
        payload["text"] = f'{text} {lang}'

    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()

    all_vacancies = response.json()

    vacancies_result = all_vacancies["items"]

    vacancies_count = all_vacancies["found"]

    vacancies_pages = all_vacancies["pages"]

    if vacancies_pages > 1:
        for page in range(1, vacancies_pages):
            payload["page"] = page

            response = requests.get('https://api.hh.ru/vacancies', params=payload)
            response.raise_for_status()

            all_vacancies = response.json()

            vacancies_result += all_vacancies["items"]

    return [vacancies_result, vacancies_count]


def predict_rub_salary(salary):
    if salary is None or salary["currency"] != "RUR":
        return None

    if salary["from"] and salary["to"]:
        return (salary["from"] + salary["to"]) / 2
    else:
        return (salary["from"] or 0) * 1.2 + (salary["to"] or 0) * 0.8