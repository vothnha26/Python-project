import pandas as pd
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from modules.ClassDesign import DataAnalyzer
from modules.treeview_table import TreeViewTable


class CRUD:
    def __init__(self, data_path):
        self.data = DataAnalyzer(data_path)
        self.file_path = data_path

    def create_data_popup(self, treeview_table: TreeViewTable):
        popup = tk.Toplevel()
        popup.title("Thêm dữ liệu mới")
        popup.geometry("300x400")
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

        date_label = tk.Label(popup, text="Ngày muốn thêm vào (YYYY-MM-DD):", bg="#f0f0f0")
        date_label.pack(pady=5)
        date_entry = tk.Entry(popup, width=30)
        date_entry.pack(pady=5)

        # Hàm xử lý khi nhấn nút lưu
        def get_who_region_and_country_code(country_name):
            country_data = self.data.data[self.data.data['Country'] == country_name]
            if not country_data.empty:
                who_region = country_data['WHO_region'].values[0]
                country_code = country_data['Country_code'].values[0]
                return who_region, country_code
            else:
                return None, None

        def check_exist_date(country_name, date):
            country_data = self.data.data[self.data.data['Country'] == country_name]
            if not country_data.empty and date in country_data['Date_reported'].values:
                return True
            return False

        def save_data():
            country = country_entry.get().strip()
            cases = cases_entry.get().strip()
            deaths = deaths_entry.get().strip()
            date_str = date_entry.get().strip()

            if not country or not cases or not deaths or not date_str:
                messagebox.showinfo("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return

            try:
                cases = int(cases)
                deaths = int(deaths)
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showinfo("Lỗi", "Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.")
                return

            # Kiểm tra ngày và quốc gia có tồn tại hay không
            if check_exist_date(country, date):
                messagebox.showinfo("Lỗi", "Ngày này đã tồn tại hoặc nước không tồn tại!")
                return

            # Lấy WHO_region và Country_code
            who_region, country_code = get_who_region_and_country_code(country)
            if who_region is None or country_code is None:
                messagebox.showinfo("Lỗi", "Không tồn tại nước này!")
                return

            # Tải và cập nhật dữ liệu
            df = self.data.data
            new_data = pd.DataFrame([{
                "Date_reported": date,
                "Country_code": country_code,
                "Country": country,
                "WHO_region": who_region,
                "New_cases": cases,
                "Cumulative_cases": 0,  # Giá trị tạm, sẽ tính sau
                "New_deaths": deaths,
                "Cumulative_deaths": 0  # Giá trị tạm, sẽ tính sau
            }])

            df = pd.concat([df, new_data], ignore_index=True)

            # Sắp xếp dữ liệu theo ngày và tính lại các giá trị tích lũy
            df['Date_reported'] = pd.to_datetime(df['Date_reported'])
            country_df = df[df['Country'] == country].sort_values(by='Date_reported')
            cumulative_cases = 0
            cumulative_deaths = 0

            for idx, row in country_df.iterrows():
                cumulative_cases += row['New_cases']
                cumulative_deaths += row['New_deaths']
                df.loc[idx, 'Cumulative_cases'] = cumulative_cases
                df.loc[idx, 'Cumulative_deaths'] = cumulative_deaths

            existing_data = df.loc[df['Date_reported'] == pd.to_datetime(date)]

            # Lưu dữ liệu vào file
            try:
                df.to_csv(self.file_path, index=False)
                treeview_table.filter_data_tree = pd.concat([treeview_table.filter_data_tree, existing_data],
                                                            ignore_index=True)
                treeview_table.current_page = 0
                treeview_table.display_treeview()
                messagebox.showinfo("Thành công", "Thêm dữ liệu thành công!")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")

        # Nút lưu dữ liệu
        save_button = tk.Button(popup, text="Lưu", command=save_data, bg="#00796b", fg="white", font=("Helvetica", 12))
        save_button.pack(pady=10)
    # def filter_data_popup(self):
