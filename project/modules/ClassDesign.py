import pandas as pd


class DataAnalyzer:
    def __init__(self):
        """
        Lớp quản lý dữ liệu từ file CSV.
        """

        self.file_path = "./data/data_clean.csv"

        self.data = pd.read_csv(self.file_path)

    def filter_data_root(self, date):
        data_root = self.data
        data_root = data_root[data_root['Date_reported'] == date]
        columns_to_include = ['Country', 'WHO_region', 'New_cases', 'Cumulative_cases', 'New_deaths',
                              'Cumulative_deaths']

        data_root = data_root[columns_to_include]  # lọc các giá trị thỏa mãn điều kiện cột đang xét
        data_root["Total_recovery"] = [int(row["Cumulative_cases"]) - int(row["Cumulative_deaths"]) for _, row in
                                       data_root.iloc[:].iterrows()]

        return data_root
