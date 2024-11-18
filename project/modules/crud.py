import pandas as pd
from typing import Dict
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from modules.treeview_table import TreeViewTable
from modules.demo_plot import ChartPlotter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modules.ClassDesign import DataAnalyzer
from modules import visualization as vs

class CRUD:
    def __init__(self, data_path):

        self.data=DataAnalyzer(data_path)

    def create_data_popup(self):
        popup = tk.Toplevel()
        popup.title("Thêm dữ liệu mới")
        popup.geometry("300x250")
        popup.configure(bg="#f0f0f0")

        # Tiêu đề
        title_label = tk.Label(popup, text="Nhập dữ liệu mới", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        country_label = tk.Label(popup, text="Tên nước:", bg="#f0f0f0")
        country_label.pack(pady=5)
        country_entry = tk.Entry(popup, width=30)
        country_entry.pack(pady=5)

        cases_label = tk.Label(popup, text="Số ca mắc mới:", bg="#f0f0f0")
        cases_label.pack(pady=5)
        cases_entry = tk.Entry(popup, width=30)
        cases_entry.pack(pady=5)

        deaths_label = tk.Label(popup, text="Số ca tử vong mới:", bg="#f0f0f0")
        deaths_label.pack(pady=5)
        deaths_entry = tk.Entry(popup, width=30)
        deaths_entry.pack(pady=5)

        date_label=tk.Label(popup,text="Ngày muốn thêm vào: ",bg="#f0f0f0")
        date_label.pack(pady=5)
        date_entry = tk.Entry(popup, width=30)
        date_entry.pack(pady=5)
        # Hàm xử lý khi nhấn nút lưu
        def get_who_region_and_country_code(country_name):
            country_data = self.data[self.data['Country'] == country_name]
            if not country_data.empty():
                who_region=country_data['WHO_region'].values[0]
                country_code = country_data['Country_code'].values[0]
                return who_region, country_code
            else:
                return None, None
        def check_exist_date(country_name,date):
            country_data = self.data[self.data['Country'] == country_name]
            if not country_data.empty():
                if date in country_data["Date_reported"]:
                    return 0
                return 1
            return 0
        def save_data():
            country = country_entry.get()
            cases = cases_entry.get()
            deaths = deaths_entry.get()
            date= date_entry.get()
            if check_exist_date(country, date)==0:
                messagebox.showinfo("Đã tồn tại ngày này hoặc nước không tồn tại!")
                return
            self.data.load_data()
            df=self.data.data
            if country in self.data.countries:
                who_region, country_code=get_who_region_and_country_code(country)
                new_data=pd.DataFrame([{
                    "Date_reported": date,
                    "Country_code": country_code,
                    "Country": country,
                    "WHO_region": who_region,
                    "New_cases": cases,
                    "Cumulative_cases": cases,
                    "New_deaths": deaths,
                    "Cumulative_deaths": deaths
                }])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                updated_df.to_csv(self.data.file_path,index=False)
                df = self.data.data
                df['Date_reported'] = pd.to_datetime(df['Date_reported'])
                country_df = df[df['Country'] == country]
                country_df = country_df.sort_values(by='Date_reported', ascending=True)
                specific_date = pd.to_datetime(date)
                previous_day_df = country_df[country_df['Date_reported'] < specific_date].iloc[-1]
                start_row_index = country_df[country_df['Date_reported'] == specific_date].index[0]
                cumulative_deaths_value = country_df.loc[start_row_index+1, 'Cumulative_deaths']
                cumulative_cases_value = country_df.loc[start_row_index+1, 'Cumulative_cases']
                country_df.loc[start_row_index, 'Cumulative_deaths'] += country_df.loc[previous_day_df, 'Cumulative_deaths']
                country_df.loc[start_row_index, 'Cumulative_cases'] += country_df.loc[previous_day_df, 'Cumulative_cases']
                for i in range(start_row_index, len(country_df)):
                    country_df.loc[i, 'Cumulative_deaths'] += cumulative_deaths_value
                    country_df.loc[i, 'Cumulative_cases'] += cumulative_cases_value
                df.update(country_df)  # Cập nhật lại dataframe gốc với các thay đổi trong country_df
                df.to_csv(self.data.file_path, index=False)

            else:
                messagebox.showinfo("Không tồn tại nước này!")
                return
            messagebox.showinfo("Thêm thành công ! ")


        # Nút lưu dữ liệu
        save_button = tk.Button(popup, text="Lưu", command=save_data, bg="#00796b", fg="white", font=("Helvetica", 12))
        save_button.pack(pady=10)

















