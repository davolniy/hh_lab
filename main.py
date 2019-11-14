from parser import Parser
from dfh import DataFrameHolder
import os

VACANCIES_PATH = 'hh_vacancies.csv'
SORTED_PATH = 'hh_sorted.csv'

p = Parser()

if os.path.exists(VACANCIES_PATH):
    vacancies_df = DataFrameHolder(path=VACANCIES_PATH)
else:
    vacancies = p.get_vacancies()
    vacancies_df = DataFrameHolder(data=vacancies)
    vacancies_df.to_csv(VACANCIES_PATH)

sorted_df = vacancies_df.salary_sort()
sorted_df.to_csv(SORTED_PATH)