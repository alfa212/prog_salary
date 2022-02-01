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
    all_vacancies = response.json()["objects"]

    vacancies_count = response.json()["total"]

    page = 0

    while response.json()["more"]:
        page += 1
        payload["page"] = page

        response = requests.get('https://api.superjob.ru/2.0/vacancies/', params=payload, headers=headers)
        response.raise_for_status()

        all_vacancies += response.json()["objects"]

    return [all_vacancies, vacancies_count]
