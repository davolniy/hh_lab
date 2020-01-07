import pandas as pd
import numpy as np
from dateutil import parser as date_parser
import ast


class DataFrameHolder(pd.DataFrame):

    def __init__(self, data=None, path=None, index=None, columns=None, dtype=None, copy=False, csv_name=None):
        if path is not None:
            pd.DataFrame.__init__(self, data=pd.read_csv(path))
        else:
            super().__init__(data, index, columns, dtype, copy)

        self.csv_name = csv_name

    @staticmethod
    def salary_sort(from_df):
        print("Salary sorting...")
        df = from_df.copy(deep=True)
        return df.sort_values(['salary_to', 'salary_from'], ascending=[True, True])

    @staticmethod
    def uniques_field_info(from_df, field):
        df = from_df[field].value_counts()

        df.csv_name = f'{field}_uniques'

        return df

    @staticmethod
    def statistics_field_info(from_df, field):
        df = DataFrameHolder()

        df[f'{field}_mean'] = from_df.mean()
        df[f'{field}_min'] = from_df.min()
        df[f'{field}_max'] = from_df.max()

        df.csv_name = f'{field}_statistics'

        return df

    @staticmethod
    def uniques_info(from_df):

        values = [v for v in from_df['key_skills'].values if len(v) > 0]
        concatenated = np.concatenate(values) if len(values) > 0 else np.empty([])

        all_key_skills = DataFrameHolder()
        all_key_skills['key_skills'] = concatenated

        salary_from_uniques_group = DataFrameHolder.uniques_field_info(from_df, 'salary_from')
        salary_to_uniques_group = DataFrameHolder.uniques_field_info(from_df, 'salary_to')
        experience_uniques_group = DataFrameHolder.uniques_field_info(from_df, 'experience')
        employment_uniques_group = DataFrameHolder.uniques_field_info(from_df, 'employment')
        schedule_uniques_group = DataFrameHolder.uniques_field_info(from_df, 'schedule')
        key_skills_uniques_group = DataFrameHolder.uniques_field_info(all_key_skills, 'key_skills')

        dfs = {
            salary_from_uniques_group.csv_name: salary_from_uniques_group,
            salary_to_uniques_group.csv_name: salary_to_uniques_group,
            experience_uniques_group.csv_name: experience_uniques_group,
            employment_uniques_group.csv_name: employment_uniques_group,
            schedule_uniques_group.csv_name: schedule_uniques_group,
            key_skills_uniques_group.csv_name: key_skills_uniques_group
        }

        return pd.concat(dfs)

    @staticmethod
    def date_info(from_df, parse_date):

        dates_odds = DataFrameHolder(
            [(parse_date - date_parser.parse(d).replace(tzinfo=None)).days for d in from_df['created_at']])

        return DataFrameHolder.statistics_field_info(dates_odds, 'days')

    @staticmethod
    def name_group_by(from_df):
        print("Grouping by name...")

        from_df['key_skills'] = from_df['key_skills'].apply(lambda x: ast.literal_eval(x) if type(x) is str else x)
        groups = from_df.groupby('name')

        return groups

    @staticmethod
    def max_salary_group_by(from_df):
        print("Grouping by max salary...")

        start = from_df['salary_to'].min()
        stop = from_df['salary_to'].max()
        step = (stop - start) / 10

        ranges = np.arange(start, stop + 1.0, step)

        from_df['key_skills'] = from_df['key_skills'].apply(lambda x: ast.literal_eval(x) if type(x) is str else x)

        groups = from_df.groupby(
            pd.cut(from_df['salary_to'], ranges)
        )

        return groups

    @staticmethod
    def concat_groups(groups, parse_date):
        uniques_groups = {}
        date_groups = {}

        for name, g in groups:
            uniques_groups[name] = DataFrameHolder.uniques_info(g)
            date_groups[name] = DataFrameHolder.date_info(g, parse_date)

        uniques_groups = DataFrameHolder(data=pd.concat(uniques_groups, keys=[k for k in uniques_groups.keys()]))
        date_groups = DataFrameHolder(data=pd.concat(date_groups, keys=[k for k in date_groups.keys()]))

        return uniques_groups, date_groups

    def display(self, max_rows=None, max_cols=None):
        with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_cols):
            print(self)
