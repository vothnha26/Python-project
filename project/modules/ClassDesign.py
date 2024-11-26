import copy
import pandas as pd


class DataAnalyzer:
    def __init__(self):
        """
        Lớp quản lý dữ liệu từ file CSV.
        """
        self.file_path = "D:\PYTHON(project)\Python-project\project\data\data_clean.csv"
        self.data = pd.read_csv(self.file_path)

    def filter_data_root(self, date):
        excluded_columns = ['Date_reported', 'Country_code']
        data_root = self.data
        data_root = data_root[data_root['Date_reported'] == date]

        # Lọc các cột cần cho TreeView
        columns_to_include = [col for col in data_root if col not in excluded_columns]

        data_root = data_root[columns_to_include]  # lọc các giá trị thỏa mãn điều kiện cột đang xét
        data_root["Total_recovery"] = [row["Cumulative_cases"] - row["Cumulative_deaths"] for _, row in
                                       data_root.iloc[:].iterrows()]

        return data_root
