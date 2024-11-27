import copy
from tkinter import ttk, messagebox
from modules.ClassDesign import DataAnalyzer
import pandas as pd

from modules.data_cleaning import clean_data

file_path = DataAnalyzer().file_path
ROWS_PER_PAGE = 1000


def convert_data(val):
    try:
        return int(val)  # Chuyển thành số nếu có thể
    except ValueError:
        return ValueError


class BaseTreeView:
    def __init__(self, frame, date='2020-01-05'):
        self.frame = frame
        self.tree = ttk.Treeview(self.frame, selectmode="extended")
        self.filter_data_tree = copy.deepcopy(DataAnalyzer().data)
        self.cal_status = False
        self.date = date

        self.tree["columns"] = ["No."] + self.filter_data_tree.columns.tolist()
        self.tree["show"] = "headings"

        # Tạo tiêu đề cho các cột
        self.tree.heading("No.", text="No.")
        self.tree.column("No.", width=50, anchor='center')

        for col in self.filter_data_tree.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview_page(c, True))
            self.tree.column(col, width=120, anchor='center')

        # Thêm thanh cuộn dọc
        self.v_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.v_scrollbar.set)
        self.v_scrollbar.pack(side='right', fill='y')

        # Thêm thanh cuộn ngang
        self.h_scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.h_scrollbar.set)
        self.h_scrollbar.pack(side='bottom', fill='x')

        # Đặt Treeview vào Frame
        self.tree.pack(expand=True, fill='both')

        # Cấu hình phân trang, hiển thị
        self.current_page = 0
        self.total_pages = len(self.filter_data_tree) // ROWS_PER_PAGE + (
            1 if len(self.filter_data_tree) % ROWS_PER_PAGE != 0 else 0)

        # Hiển thị thứ tự trang hiện tại
        self.page_label = ttk.Label(frame, text="")
        self.page_label.place(x=290, y=437)

        # Tạo nút reset
        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.restore_data_root)
        self.reset_button.place(x=290, y=680)

    def display_treeview(self):
        self.update_total_pages()
        self.update_page_label()
        """Hiển thị dữ liệu lên Treeview theo trang, bao gồm cột thứ tự."""
        self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ
        start = self.current_page * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE

        for i, (_, row) in enumerate(self.filter_data_tree.iloc[start:end].iterrows(), start=1):
            self.tree.insert("", "end", values=[start + i] + list(row))

    def update_page_label(self):
        """Cập nhật nhãn hiển thị số trang."""
        self.page_label.config(text=f"Page {self.current_page + 1} of {self.total_pages}")

    def update_total_pages(self):
        self.total_pages = len(self.filter_data_tree) // ROWS_PER_PAGE + (
            1 if len(self.filter_data_tree) % ROWS_PER_PAGE != 0 else 0)

    def sort_treeview_page(self, col, descending):
        """Sắp xếp dữ liệu trên bảng phân trang."""
        data = [(convert_data(self.tree.set(item, col)), item) for item in self.tree.get_children()]
        data = sorted(data, reverse=descending)

        for index, (_, item) in enumerate(data):
            self.tree.move(item, '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview_page(col, not descending))

    def sort_all_data(self, descending):
        """"Sắp xếp toàn bộ trang trong bảng."""
        self.filter_data_tree = self.filter_data_tree.sort_values(['Cumulative_cases', 'Cumulative_deaths'],
                                                                  ascending=descending)

        self.current_page = 0
        self.display_treeview()

    def filter_tree(self, filter_area: dict, filter_year: dict):
        self.current_page = 0
        # Khởi tạo các danh sách khu vực và thời gian đã được tick tại checkbutton
        option_area = []
        option_year = []
        for area, var in filter_area.items():
            if var.get() is True:
                option_area.append(area)

        for year, var in filter_year.items():
            if var.get() is True:
                option_year.append(year)

        if len(option_area) + len(option_year) == 0:
            return

        if len(option_year) == 0:
            option_year = ['2020', '2021', '2022', '2023', '2024']

        if len(option_area) == 0:
            option_area = ['AMRO', 'WPRO', 'EURO', 'SEARO', 'AFRO', 'EMRO', 'OTHER']
        """"Bộ lọc toàn bộ trang"""
        self.current_page = 0
        compare = lambda x, y: x.isin(y)

        # Kiểm tra self đang thuộc lớp nào để thực hiện điều kiện so sánh thích hợp
        if self.cal_status is False:
            self.filter_data_tree = self.filter_data_tree[
                compare(self.filter_data_tree["WHO_region"], option_area) & compare(
                    self.filter_data_tree["Date_reported"].str[:4],
                    option_year)]
        else:
            self.filter_data_tree = self.filter_data_tree[
                compare(self.filter_data_tree["WHO_region"], option_area)]

        self.display_treeview()

    def search_country_tree(self, country_name: str, date: str):
        self.current_page = 0
        """Tìm kiếm và hiển thị kết quả trong Treeview."""

        if country_name == '' and date == '':
            return

        if country_name == '':
            self.filter_data_tree = self.filter_data_tree[self.filter_data_tree["Date_reported"] == date]

        # Tìm chuỗi con trong Country
        def country_matches(row):
            n = len(row["Country"])
            m = len(country_name)

            for i in range(n - m + 1):
                if row["Country"][i:i + m] == country_name:
                    return True

            return False

        self.filter_data_tree = self.filter_data_tree[self.filter_data_tree.apply(country_matches, axis=1)]

        if date != '':
            self.filter_data_tree = self.filter_data_tree[self.filter_data_tree["Date_reported"] == date]
        self.display_treeview()

    def restore_data_root(self):
        """"Trả về dữ liệu ban đầu."""
        self.filter_data_tree = pd.read_csv(file_path) if self.cal_status is False else DataAnalyzer().filter_data_root(
            self.date)
        self.current_page = 0
        self.display_treeview()

    def delete_selected(self):
        selected_item = self.tree.selection()  # Lấy item đang được chọn

        if selected_item:
            for i, item in enumerate(selected_item):
                # Xóa dòng dữ liệu trong filter_data_tree
                row_index = int(self.tree.item(item, "values")[0]) - 1 - i
                self.filter_data_tree.drop(self.filter_data_tree.index[row_index], inplace=True)
                self.tree.delete(item)  # Xóa item khỏi TreeView

    def save_updated_data(self, no=None, cases_entry=None, deaths_entry=None, date_entry=None, country=None, popup=None,
                          country_code=None, who_region=None):
        """Cập nhật dữ liệu vào CSV và TreeView."""
        try:
            # Lấy thông tin từ giao diện người dùng
            new_cases = int(cases_entry.get().strip())
            new_deaths = int(deaths_entry.get().strip())
            date = pd.to_datetime(date_entry.get().strip()).strftime('%Y-%m-%d')  # Đảm bảo chỉ có ngày (YYYY-MM-DD)

            # Kiểm tra nếu DataFrame rỗng
            if self.filter_data_tree.empty:
                messagebox.showerror("Lỗi", "Không có dữ liệu trong bảng để cập nhật.")
                return

            df = DataAnalyzer().data

            # Kiểm tra hàng khớp điều kiện
            matching_rows = df[(df['Country'].str.strip() == country.strip()) & (df['Date_reported'] == date)]
            if matching_rows.empty:
                messagebox.showerror("Lỗi", "Không tìm thấy dòng dữ liệu phù hợp để cập nhật.")
                return

            # Cập nhật dữ liệu mới
            df.loc[
                (df['Country'].str.strip() == country.strip()) & (df['Date_reported'] == date), 'New_cases'] = new_cases
            df.loc[(df['Country'].str.strip() == country.strip()) & (
                    df['Date_reported'] == date), 'New_deaths'] = new_deaths

            # Sắp xếp dữ liệu theo ngày và tính lại các giá trị tích lũy
            df['Date_reported'] = pd.to_datetime(df['Date_reported']).dt.strftime('%Y-%m-%d')  # Đảm bảo chỉ có ngày
            country_df = df[df['Country'] == country].sort_values(by='Date_reported')

            for idx, row in country_df.iterrows():
                if row['Date_reported'] >= date:
                    df.loc[idx, 'Cumulative_cases'] += new_cases
                    df.loc[idx, 'Cumulative_deaths'] += new_deaths

            # Lấy tổng số ca và tử vong tích lũy tại ngày được cập nhật
            updated_row = df.loc[(df['Country'].str.strip() == country.strip()) & (df['Date_reported'] == date)]
            total_of_case = updated_row['Cumulative_cases'].iloc[0]
            total_of_death = updated_row['Cumulative_deaths'].iloc[0]

            # Lưu dữ liệu vào CSV
            data_save = DataAnalyzer().data
            data_save[data_save['Country'].str.strip() == country.strip()] = df
            data_save.to_csv(file_path, index=False)
            clean_data(file_path, file_path)

            # Cập nhật lại TreeView mà không xóa
            selected_item = self.tree.selection()[0]  # Lấy item đang được chọn
            updated_row = (
                no, date, country_code, country, who_region, new_cases, total_of_case, new_deaths, total_of_death)
            self.tree.item(selected_item, values=updated_row)  # Cập nhật số liệu mới cho hàng hiện tại

            # Cập nhật DataFrame nội bộ
            self.filter_data_tree = DataAnalyzer().filter_data_root(self.date)

            self.display_treeview()

            # Hiển thị thông báo thành công
            messagebox.showinfo("Thành công", "Cập nhật dữ liệu thành công!")
            popup.destroy()  # Đóng popup sau khi cập nhật

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")


class TreeViewTable(BaseTreeView):
    def __init__(self, frame):
        super().__init__(frame)

        # tạo các nút phân trang
        self.next_button = ttk.Button(frame, text="Next", command=self.next_page)
        self.next_button.place(x=585, y=427)

        self.pre_button = ttk.Button(self.frame, text="Previous", command=self.prev_page)
        self.pre_button.place(x=0, y=427)

    def prev_page(self):
        """Chuyển về trang trước."""
        if self.current_page > 0:
            self.current_page -= 1
            self.display_treeview()

    def next_page(self):
        """Chuyển sang trang tiếp theo."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_treeview()
