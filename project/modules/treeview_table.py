import copy
from tkinter import ttk, messagebox
import tkinter as tk
from modules.ClassDesign import DataAnalyzer
import pandas as pd

file_path = './data/data_clean.csv'
ROWS_PER_PAGE = 1000
MOD = 1003


def convert_data(val):
    try:
        return int(val)  # Chuyển thành số nếu có thể
    except ValueError:
        return ValueError


class BaseTreeView:
    def __init__(self, frame, excluded_columns=None, filter_condition=None):
        self.frame = frame
        self.tree = ttk.Treeview(self.frame, selectmode="extended")
        self.excluded_columns = excluded_columns or []
        self.data_root = DataAnalyzer(file_path).data

        if filter_condition:
            self.data_root = self.data_root[filter_condition]  # lọc các giá trị thỏa mãn điều kiện cột đang xét

        # Lọc các cột cần cho TreeView
        self.columns_to_include = [col for col in self.data_root if col not in self.excluded_columns]
        self.data_root = self.data_root[self.columns_to_include]
        self.filter_data_tree = copy.deepcopy(self.data_root)

        self.tree["columns"] = ["No."] + self.columns_to_include
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

    def filter_tree(self, selected_value: str, option: list):
        """"Bộ lọc toàn bộ trang"""
        self.current_page = 0
        if selected_value == "WHO_region":
            compare = lambda x, y: x.isin(y)
        else:
            compare = lambda x, y: x > 100 and y < 1000

        self.filter_data_tree = self.filter_data_tree[
            compare(self.filter_data_tree[selected_value], option)]

        self.display_treeview()

    def create_search(self):
        self.current_page = 0

        popup = tk.Toplevel()
        popup.title("Tìm kiếm")
        popup.geometry("300x400")
        popup.configure(bg="#f0f0f0")

        # Tiêu đề
        title_label = tk.Label(popup, text="Tìm kiếm", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)
        country_label = tk.Label(popup, text="Tên nước:", bg="#f0f0f0")
        country_label.pack(pady=5)
        country_entry = tk.Entry(popup, width=30)
        country_entry.pack(pady=5)

        # Nút lưu dữ liệu
        find_button = tk.Button(popup, text="Tìm kiếm",
                                command=lambda: self.search_country_tree(country_entry.get().strip()),
                                bg="#00796b", fg="white", font=("Helvetica", 12))
        find_button.pack(pady=10)

    def search_country_tree(self, country_name: str):
        """Tìm kiếm và hiển thị kết quả trong Treeview."""
        self.current_page = 0

        def country_matches(row):
            n = len(row["Country"])
            m = len(country_name)

            for i in range(n - m + 1):
                if row["Country"][i:i + m] == country_name:
                    return True

            return False

        self.filter_data_tree = self.filter_data_tree[self.filter_data_tree.apply(country_matches, axis=1)]
        self.display_treeview()

    def clear_treeview(self):
        """Hủy bỏ toàn bộ Treeview cũ và thanh cuộn."""
        # Xóa Treeview cũ
        self.tree.destroy()

        # Xóa thanh cuộn
        self.v_scrollbar.destroy()

        # Xóa nhãn
        self.page_label.destroy()

        # Xóa tham chiếu đối tượng
        del self.tree
        del self.v_scrollbar
        del self.page_label

    def restore_data_root(self):
        """"Trả về dữ liệu ban đầu."""
        self.filter_data_tree = self.data_root
        self.current_page = 0
        self.display_treeview()


class TreeViewTable(BaseTreeView):
    def __init__(self, frame):
        super().__init__(frame)

        # tạo các nút phân trang
        self.next_button = ttk.Button(frame, text="Next", command=self.next_page)
        self.next_button.place(x=585, y=427)

        self.pre_button = ttk.Button(self.frame, text="Previous", command=self.prev_page)
        self.pre_button.place(x=0, y=427)
    def delete_selected(self):
        selected_item = self.tree.selection()  # Lấy item đang được chọn
        if selected_item:
            for item in selected_item:
                # Xóa dòng dữ liệu trong filter_data_tree
                row_index = int(self.tree.item(item, "values")[0]) - 1
                self.filter_data_tree.drop(self.filter_data_tree.index[row_index], inplace=True)
                self.tree.delete(item)  # Xóa item khỏi TreeView

            # Cập nhật lại số trang và nhãn trang hiện tại sau khi xóa dữ liệu
            self.update_total_pages()
            self.update_page_label()

    def next_page(self):
        """Chuyển sang trang tiếp theo."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_treeview()

    def prev_page(self):
        """Chuyển về trang trước."""
        if self.current_page > 0:
            self.current_page -= 1
            self.display_treeview()

    def save_updated_data(self, no, cases_entry, deaths_entry, date_entry, country, popup, country_code, who_region):
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

            df = self.filter_data_tree

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

            cumulative_cases = 0
            cumulative_deaths = 0

            for idx, row in country_df.iterrows():
                cumulative_cases += row['New_cases']
                cumulative_deaths += row['New_deaths']
                df.loc[idx, 'Cumulative_cases'] = cumulative_cases
                df.loc[idx, 'Cumulative_deaths'] = cumulative_deaths

            # Lấy tổng số ca và tử vong tích lũy tại ngày được cập nhật
            updated_row = df.loc[(df['Country'].str.strip() == country.strip()) & (df['Date_reported'] == date)]
            TotalOfCase = updated_row['Cumulative_cases'].iloc[0]
            TotalOfDeath = updated_row['Cumulative_deaths'].iloc[0]

            # Lưu dữ liệu vào CSV
            df.to_csv(file_path, index=False)

            # Cập nhật lại TreeView mà không xóa
            selected_item = self.tree.selection()[0]  # Lấy item đang được chọn
            updated_row = (
            no, date, country_code, country, who_region, new_cases, TotalOfCase, new_deaths, TotalOfDeath)
            self.tree.item(selected_item, values=updated_row)  # Cập nhật số liệu mới cho hàng hiện tại

            # Cập nhật DataFrame nội bộ
            self.filter_data_tree = df

            self.display_treeview()

            # Hiển thị thông báo thành công
            messagebox.showinfo("Thành công", "Cập nhật dữ liệu thành công!")
            popup.destroy()  # Đóng popup sau khi cập nhật

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")


class TreeViewFilter(BaseTreeView):
    def __init__(self, frame, date='2020-01-05'):
        self.date = date
        super().__init__(frame, excluded_columns=['Date_reported', 'Country_code'],
                         filter_condition=self.filter_condition)

    def filter_condition(self, data):
        return data['Date_reported'] == self.date
