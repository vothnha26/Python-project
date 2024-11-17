import pandas as pd
from typing import Dict
import matplotlib.pyplot as plt
class Country:
    def __init__(self, who_region: str, country: str, country_code: str, report : pd.DataFrame):
        """
        Lớp đại diện cho một quốc gia.
        """
        self.WHO_region = who_region
        self.Country = country
        self.Country_code = country_code
        self.Report = report

    def add_report(self, date_reported, new_cases, cumulative_cases, new_deaths, cumulative_deaths):
        """
        Thêm một báo cáo mới vào dữ liệu quốc gia.
        """
        new_data = {
            "Date_reported": date_reported,
            "New_cases": new_cases,
            "Cumulative_cases": cumulative_cases,
            "New_deaths": new_deaths,
            "Cumulative_deaths": cumulative_deaths,
        }
        self.Report = pd.concat([self.Report, pd.DataFrame([new_data])], ignore_index=True)
    def get_total_cases(self) -> int:
        return self.report["Cumulative_cases"].iloc[-1] if not self.Report.empty else 0

    def get_total_deaths(self) -> int:
        return self.report["Cumulative_deaths"].iloc[-1] if not self.Report.empty else 0

    def get_new_cases(self):
        return self.report["New_cases"] if "New_cases" in self.Report.columns else pd.Series()

class Region:
    def __init__(self, who_region: str):
        """
        Lớp đại diện cho một khu vực WHO.
        """
        self.WHO_region = who_region
        self.Countries: Dict[str, Country] = {}

    def add_country(self, country: Country):
        """
        Thêm một quốc gia vào khu vực.
        """
        if country.Country not in self.Countries:
            self.Countries[country.Country] = country # lấy tên quốc gia làm key


class DataAnalyzer:
    def __init__(self, file_path):
        """
        Lớp quản lý dữ liệu từ file CSV.
        """
        self.file_path = file_path
        self.data = None
        self.countries: Dict[str, Country] = {}
        self.regions: Dict[str, Region] = {}

    def load_data(self):
        """
        Tải dữ liệu từ file CSV và tổ chức thành các đối tượng Country và Region.
        """
        self.data = pd.read_csv(self.file_path)

        # Lặp qua từng dòng trong DataFrame
        for _, row in self.data.iterrows():
            # Tạo hoặc lấy quốc gia
            country = self.get_or_create_country(
                row["Country"], row["WHO_region"], row["Country_code"]
            )

            # Thêm dữ liệu báo cáo vào quốc gia
            country.add_report(
                row["Date_reported"],
                row["New_cases"],
                row["Cumulative_cases"],
                row["New_deaths"],
                row["Cumulative_deaths"],
            )

    def get_or_create_country(self, country_name: str, who_region: str, country_code: str) -> Country:
        if country_name in self.countries:
            return self.countries[country_name]

        # Tạo mới quốc gia với report là DataFrame rỗng
        country = Country(who_region, country_name, country_code, pd.DataFrame(columns=["Date_reported", "New_cases", "Cumulative_cases", "New_deaths", "Cumulative_deaths"]))
        self.countries[country_name] = country

        # Kiểm tra khu vực WHO
        if who_region not in self.regions:
            self.regions[who_region] = Region(who_region)

        # Thêm quốc gia vào khu vực
        self.regions[who_region].add_country(country)

        return country
    
   