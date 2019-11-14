import requests
import mapper
from tqdm import tqdm


class Parser:

    URL_VACANCIES = 'https://api.hh.ru/vacancies?'
    URL_VACANCY = 'https://api.hh.ru/vacancies/'
    PER_PAGE = 100
    PAGES = 10
    PBAR_UPDATE = 10

    def get_vacancies(self):
        params = {'area': 1, 'text': 'Программист', "per_page": Parser.PER_PAGE}

        vacancies = []

        pbar = tqdm(total=Parser.PER_PAGE * Parser.PAGES)

        print(f'Parcing vacancies from {Parser.URL_VACANCIES}')
        for i in range(Parser.PAGES):
            params["page"] = i
            vacancies_json = requests.get(Parser.URL_VACANCIES, params).json()["items"]

            for j in range(len(vacancies_json)):
                v = requests.get(Parser.URL_VACANCY + vacancies_json[j]["id"]).json()
                v["snippet"] = {}
                v["snippet"]["responsibility"] = vacancies_json[j]["snippet"]["responsibility"]
                v["snippet"]["requirement"] = vacancies_json[j]["snippet"]["requirement"]

                vacancy = mapper.ResponseToVacancyMapper.map(v)

                vacancies.append(vacancy)

                if j % Parser.PBAR_UPDATE == 0:
                    pbar.update(Parser.PBAR_UPDATE)


        return vacancies
