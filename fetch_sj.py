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


def predict_rub_salary_for_superJob(vacancy):
    if vacancy["payment_from"] + vacancy["payment_to"] == 0 or vacancy["currency"] != "rub":
        return None

    if vacancy["payment_from"] and vacancy["payment_to"]:
        return (vacancy["payment_from"] + vacancy["payment_to"]) / 2
    else:
        return (vacancy["payment_from"] or 0) * 1.2 + (vacancy["payment_to"] or 0) * 0.8