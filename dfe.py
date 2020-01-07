import os
from dfh import DataFrameHolder


class DataFrameEditor:

    def __init__(self, dir_path=''):
        self.dir_path = dir_path

        if dir_path != '' and not os.path.exists(dir_path):
            os.mkdir(dir_path)

    def get_full_path(self, csv_name):
        return f"{self.dir_path}/{csv_name}"

    def write_df(self, df):
        full_path = self.get_full_path(df.csv_name)
        df.to_csv(full_path)

    def write_dfs(self, dfs):
        for df in dfs:
            self.write_df(df)

    def write_groups(self, groups, csv_name):
        full_path = self.get_full_path(csv_name)

        if not os.path.exists(full_path):
            os.mkdir(full_path)

        groups_editor = DataFrameEditor(full_path)

        for g in groups:
            groups_editor.write_df(g)

    def init_df(self, csv_name, data_extractor, force=False):

        full_path = self.get_full_path(csv_name)

        if os.path.exists(full_path) and not force:
            df = DataFrameHolder(path=full_path, csv_name=csv_name)
        else:
            if callable(data_extractor):
                df = DataFrameHolder(data=data_extractor(), csv_name=csv_name)
            else:
                df = DataFrameHolder(data=data_extractor, csv_name=csv_name)

            self.write_df(df)

        return df
