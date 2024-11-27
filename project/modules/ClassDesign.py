import pandas as pd
import copy


class DataAnalyzer:
    def __init__(self):
        """
        Lớp quản lý dữ liệu từ file CSV.
        """
        self.file_path = "./data/data_clean.csv"

        self.data = pd.read_csv(self.file_path)
        self.data['Total_recovery'] = self.data['Cumulative_cases'].astype(int) - self.data['Cumulative_deaths'].astype(
            int)

    def filter_data_root(self, date):
        data_root = copy.deepcopy(self.data)
        return data_root[data_root['Date_reported'] == date]
