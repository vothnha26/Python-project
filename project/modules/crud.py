import pandas as pd
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from modules.ClassDesign import DataAnalyzer
from modules.treeview_task import TreeViewTable


class CRUD:
    def __init__(self):
        self.data = DataAnalyzer()
        self.file_path = DataAnalyzer().file_path

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
            # Kiểm tra xem ngày đã tồn tại trong dữ liệu của quốc gia này hay chưa
            country_data = self.data.data[self.data.data['Country'] == country_name]
            if not country_data.empty:
                # Kiểm tra xem quốc gia và ngày có tồn tại không (so sánh với định dạng chuẩn)
                country_data['Date_reported'] = pd.to_datetime(country_data['Date_reported']).dt.date
                if date in country_data['Date_reported'].values:
                    return True  # Ngày đã tồn tại trong quốc gia này
            return False

        def save_data():
            country = country_entry.get().strip()
            cases = cases_entry.get().strip()
            deaths = deaths_entry.get().strip()
            date_str = date_entry.get().strip()
            if int(cases_entry.get()) < 0 or int(deaths_entry.get()) < 0:
                messagebox.showerror("Lỗi", "Không được nhập số âm!!")
                return
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
                messagebox.showinfo("Lỗi", "Ngày này đã tồn tại trong dữ liệu của quốc gia này!")
                return  # Thoát ra mà không thêm dữ liệu

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
                if row['Date_reported'].strftime("%Y-%m-%d") == str(date):
                    new_data['Cumulative_cases'] += cumulative_cases
                    new_data['Cumulative_deaths'] += cumulative_deaths

                cumulative_cases += row['New_cases']
                cumulative_deaths += row['New_deaths']
                df.loc[idx, 'Cumulative_cases'] = cumulative_cases
                df.loc[idx, 'Cumulative_deaths'] = cumulative_deaths

            # Cập nhật lại dữ liệu sau khi tính giá trị tích lũy
            existing_data = df.loc[(df['Date_reported'] == pd.to_datetime(date))]
            existing_data['Date_reported'] = existing_data['Date_reported'].dt.strftime('%Y-%m-%d')

            # Lưu dữ liệu vào file
            try:
                # Ghi chuỗi rỗng vào file
                df.to_csv(self.file_path, index=False)
                treeview_table.filter_data_tree = existing_data if treeview_table.cal_status is False else DataAnalyzer().filter_data_root(
                    str(date))

                self.data.data = df
                treeview_table.display_treeview()
                messagebox.showinfo("Thành công", "Thêm dữ liệu thành công!")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")

        # Nút lưu dữ liệu
        save_button = tk.Button(popup, text="Lưu", command=save_data, bg="#00796b", fg="white", font=("Helvetica", 12))
        save_button.pack(pady=10)

    def update_data_popup(self, treeview_table):
        """Tạo popup để cập nhật dữ liệu được chọn."""
        selected_item = treeview_table.tree.selection()
        if not selected_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một hàng để cập nhật.")
            return

        # Lấy dữ liệu từ hàng được chọn
        item_data = treeview_table.tree.item(selected_item[0])
        row_values = item_data['values']
        no, date_reported, country_code, country, who_region, new_cases, cumulative_cases, new_deaths, cumulative_deaths, _ = row_values

        popup = tk.Toplevel()
        popup.title("Cập nhật dữ liệu")
        popup.geometry("300x400")
        popup.configure(bg="#f0f0f0")

        # Tạo các ô nhập liệu với giá trị hiện tại
        labels_entries = [
            ("Ngày báo cáo:", date_reported),
            ("Tên nước:", country),
            ("Số ca mắc mới:", new_cases),
            ("Số ca tử vong mới:", new_deaths),
        ]
        entries = []
        for label_text, default_value in labels_entries:
            tk.Label(popup, text=label_text, bg="#f0f0f0").pack(pady=5)
            entry = tk.Entry(popup, width=30)
            entry.insert(0, default_value)
            entry.pack(pady=5)
            entries.append(entry)

        date_entry, country_entry, cases_entry, deaths_entry = entries

        # Nút Lưu
        def update_command():
            treeview_table.save_updated_data(no, date_reported, cases_entry, deaths_entry, date_entry, country, popup,
                                             country_code,
                                             who_region)

        save_button = tk.Button(popup, text="Lưu", command=update_command, bg="#00796b", fg="white",
                                font=("Helvetica", 12))
        save_button.pack(pady=10)

    def delete_multiple_data(self, treeview_table):
        # Lấy tất cả các hàng đã chọn trong TreeView
        selected_items = treeview_table.tree.selection()
        if not selected_items:
            messagebox.showinfo("Thông báo", "Vui lòng chọn ít nhất một hàng để xóa.")
            return

        # Xác nhận xóa nhiều hàng
        confirm = messagebox.askyesno("Xác nhận",
                                      f"Bạn có chắc chắn muốn xóa {len(selected_items)} hàng đã chọn?")
        if not confirm:
            return

        # Lấy dữ liệu của các hàng đã chọn
        rows_to_delete = []
        for selected_item in selected_items:
            item_data = treeview_table.tree.item(selected_item)
            row_values = item_data['values']
            date_reported, country_code, country, who_region, new_cases, cumulative_cases, new_deaths, cumulative_deaths = row_values[
                                                                                                                           1:9]
            rows_to_delete.append((date_reported, country))

        # Chuyển đổi ngày báo cáo về dạng datetime và tìm các hàng cần xóa trong DataFrame
        df = self.data.data
        for date_reported, country in rows_to_delete:
            date_reported = pd.to_datetime(date_reported).strftime('%Y-%m-%d')
            # df = df[~((df['Date_reported'] == date_reported) & (df['Country'] == country))]
            df = df.drop(df[(df['Date_reported'] == date_reported) & (df['Country'] == country)].index)

        # Cập nhật lại các giá trị tích lũy cho các quốc gia sau khi xóa
        for date_reported, country in rows_to_delete:
            country_df = df[df['Country'] == country].sort_values(by='Date_reported')
            cumulative_cases = 0
            cumulative_deaths = 0
            for idx, row in country_df.iterrows():
                cumulative_cases += row['New_cases']
                cumulative_deaths += row['New_deaths']
                df.at[idx, 'Cumulative_cases'] = cumulative_cases
                df.at[idx, 'Cumulative_deaths'] = cumulative_deaths

        # Lưu dữ liệu vào CSV
        try:
            self.data.data = df  # Cập nhật dữ liệu trong DataAnalyzer
            df.to_csv(self.file_path, index=False)

            # Xóa các hàng trong TreeView
            treeview_table.delete_selected()
            treeview_table.filter_data_tree=df
            # Cập nhật lại TreeView với dữ liệu mới
            treeview_table.display_treeview()

            messagebox.showinfo("Thành công", "Đã xóa các dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")
