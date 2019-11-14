import pandas as pd
from tqdm import tqdm


class DataFrameHolder(pd.DataFrame):

    def __init__(self, path=None, data=None, index=None, columns=None, dtype=None, copy=False):
        if path is not None:
            pd.DataFrame.__init__(self, data=pd.read_csv(path))
        else:
            super().__init__(data, index, columns, dtype, copy)

    def salary_sort(self):
        print("Salary sorting...")
        copy = self.copy(True)
        return copy.sort_values(['salary_to', 'salary_from'], ascending=[True, True])

    def max_salary_group_by(self, field, count):

        max_salaries = self[self[field].nonzero()]

        sliced = [self[field].loc[i: i + count - 1] for i in range(0, len(self[field]), count)]

        return self.lo

    def unique_field_count(self, group, field):
        uniques = self[field].unique()

        print(' processing: ')
        groups = self.groupby(field)[field].count()
        return groups.groupby(level=0).apply(lambda x: x)

    def calculate(self):

        print('Fields processing: ')
        for field in tqdm(self.columns):

            current = self[field]

    def display(self, max_rows=None, max_cols=None):
        with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_cols):
            print(self)
