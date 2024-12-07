import pandas as pd
import copy
from datetime import datetime


class DataAnalyzer:
    def __init__(self):
        """
        Lớp quản lý dữ liệu từ file CSV.
        """
        self.file_path = "./data/data_clean.csv"

        self.data = pd.read_csv(self.file_path)
        self.data['Total_alive'] = self.data['Cumulative_cases'].astype(int) - self.data['Cumulative_deaths'].astype(
            int)

    def filter_data_root(self, date):
        data_root = copy.deepcopy(self.data)
        return data_root[data_root['Date_reported'] == date]

    def is_valid_date(date_str: str):
        """Kiểm tra ngày tháng có đúng định dạng YYYY-MM-DD hay không."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
