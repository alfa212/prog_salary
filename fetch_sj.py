import requests


def fetch_sj_vacancies_info(headers, lang=''):
    payload = {
        "town": "Москва",
        "catalogues": 48,
        "count": 100
    }

    if lang:
        payload["keywords[0][srws]"] = 1
        payload["keywords[0][skwc]"] = "and"
        payload["keywords[0][keys]"] = lang

    response = requests.get('https://api.superjob.ru/2.0/vacancies/', params=payload, headers=headers)
    response.raise_for_status()

    info_from_api = response.json()

    all_vacancies = info_from_api["objects"]

    vacancies_count = info_from_api["total"]

    page = 0

    while info_from_api["more"]:
        page += 1
        payload["page"] = page

        response = requests.get('https://api.superjob.ru/2.0/vacancies/', params=payload, headers=headers)
        response.raise_for_status()

        info_from_api = response.json()

        all_vacancies += info_from_api["objects"]

    return [all_vacancies, vacancies_count]
