import requests
import mapper
from tqdm import tqdm

class Parser:
    URL_VACANCIES = 'https://api.hh.ru/vacancies?'
    URL_VACANCY = 'https://api.hh.ru/vacancies/'
    PBAR_UPDATE = 10

    def get_vacancies(self, area=1, text='Программист', pages=10, per_page=100):
        params = {'area': area, 'text': text, "per_page": per_page}

        vacancies = []

        pbar = tqdm(total=per_page * pages, desc=f'Parcing vacancies from {Parser.URL_VACANCIES}')

        for i in range(pages):
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
