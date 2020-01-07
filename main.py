from parsers import Parser
from dfh import DataFrameHolder
from dfe import DataFrameEditor
from datetime import datetime
from dateutil import parser as date_parser


VACANCIES_NAME = 'hh_vacancies.csv'
SORTED_NAME = 'hh_sorted.csv'
MAX_SALARY_GROUPS_NAME = 'hh_max_salary_groups.csv'
MAX_SALARY_DATE_ODDS_NAME = 'hh_max_salary_date_odds.csv'
NAME_GROUPS_NAME = 'hh_name_groups.csv'
NAME_DATE_ODS_NAME = 'hh_name_date_odds.csv'
DATAFRAMES_PATH = 'dataframes'
SOURCES_DATAFRAMES_PATH = f"{DATAFRAMES_PATH}/sources"
SORTED_DATAFRAMES_PATH = f"{DATAFRAMES_PATH}/sorted"
GROUPED_DATAFRAMES_PATH = f"{DATAFRAMES_PATH}/grouped"


def init(force=False):
    DataFrameEditor(DATAFRAMES_PATH)
    origin_editor = DataFrameEditor(SOURCES_DATAFRAMES_PATH)
    sorted_editor = DataFrameEditor(SORTED_DATAFRAMES_PATH)
    groups_editor = DataFrameEditor(GROUPED_DATAFRAMES_PATH)

    p = Parser()
    parse_date = date_parser.parse(datetime.today().isoformat())

    vacancies_df = origin_editor.init_df(
        VACANCIES_NAME,
        p.get_vacancies,
        force)

    sorted_df = sorted_editor.init_df(
        SORTED_NAME,
        DataFrameHolder.salary_sort(vacancies_df),
        force)

    max_salary_groups, max_salary_date_odds = DataFrameHolder.concat_groups(
        DataFrameHolder.max_salary_group_by(sorted_df), parse_date)

    max_salary_groups_df = groups_editor.init_df(
        MAX_SALARY_GROUPS_NAME,
        max_salary_groups,
        force)

    max_salary_date_odds_df = groups_editor.init_df(
        MAX_SALARY_DATE_ODDS_NAME,
        max_salary_date_odds,
        force)

    name_groups, name_date_odds = DataFrameHolder.concat_groups(
        DataFrameHolder.name_group_by(sorted_df), parse_date)

    name_groups_df = groups_editor.init_df(
        NAME_GROUPS_NAME,
        name_groups,
        force)

    name_date_odds_df = groups_editor.init_df(
        NAME_DATE_ODS_NAME,
        name_date_odds,
        force)


init(False)
