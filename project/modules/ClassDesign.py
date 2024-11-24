import pandas as pd
from typing import Dict


class Country:
    def __init__(self, who_region, country, country_code, new_cases, cumulative_cases, new_deaths, cumulative_deaths):
        """
        Lớp đại diện cho một quốc gia.
        """
        self.WHO_region = who_region
        self.Country = country
        self.Country_code = country_code
        self.New_case = int(new_cases)
        self.Cumulative_cases = int(cumulative_cases)
        self.New_deaths = int(new_deaths)
        self.Cumulative_deaths = int(cumulative_deaths)

class DataAnalyzer:
    def __init__(self, file_path):
        """
        Lớp quản lý dữ liệu từ file CSV.
        """
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)
        self.countries: Dict[str, Country] = {}
        self.regions: Dict[str, Country] = {}

        """
        Tải dữ liệu từ file CSV và tổ chức thành các đối tượng Country.
        """
        for _, row in self.data.iterrows():
            country = self.get_or_create_country(
                row["Country"], 
                row["WHO_region"], 
                row["Country_code"],
                row["New_cases"],
                row["Cumulative_cases"],
                row["New_deaths"],
                row["Cumulative_deaths"],
            )

    def get_or_create_country(self, country_name, who_region, country_code, new_cases, cumulative_cases, new_deaths, cumulative_deaths):
        """
        Lấy quốc gia nếu đã tồn tại, nếu chưa tạo mới.
        """
        if country_name in self.countries:
            self.countries[country_name].New_case += new_cases
            self.countries[country_name].Cumulative_cases += cumulative_cases
            self.countries[country_name].New_deaths += new_deaths
            self.countries[country_name].Cumulative_deaths += cumulative_deaths
        else:
            self.countries[country_name] = Country(who_region, country_name, country_code, new_cases, cumulative_cases, new_deaths, cumulative_deaths)
        
        if country_code in self.countries:
            self.countries[country_code].New_case += new_cases
            self.countries[country_code].Cumulative_cases += cumulative_cases
            self.countries[country_code].New_deaths += new_deaths
            self.countries[country_code].Cumulative_deaths += cumulative_deaths
        else:
            self.countries[country_code] = Country(who_region, country_name, country_code, new_cases, cumulative_cases, new_deaths, cumulative_deaths)

