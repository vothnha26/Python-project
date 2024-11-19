import copy
from tkinter import ttk
from modules.ClassDesign import DataAnalyzer

file_path = './data/data.csv'
ROWS_PER_PAGE = 1000


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

        # Đặt Treeview vào Frame
        self.tree.pack(expand=True, fill='both')

        # Cấu hình phân trang, hiển thị
        self.current_page = 0
        self.total_pages = len(self.filter_data_tree) // ROWS_PER_PAGE + (
            1 if len(self.filter_data_tree) % ROWS_PER_PAGE != 0 else 0)

        # Hiển thị thứ tự trang hiện tại
        self.page_label = ttk.Label(frame, text="")
        self.page_label.place(x=470, y=437)

        # Tạo nút reset
        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.restore_data_root)
        self.reset_button.place(x=470, y=680)

    def display_treeview(self):
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

    def load_display(self):
        self.update_total_pages()
        self.update_page_label()
        self.display_treeview()

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
        self.load_display()

    def filter_tree(self, selected_value: str, option: list):
        """"Bộ lọc toàn bộ trang"""
        self.current_page = 0
        if selected_value == "WHO_region":
            compare = lambda x, y: x.isin(y)
        else:
            compare = lambda x, y: x > 100 and y < 1000

        self.filter_data_tree = self.filter_data_tree[
            compare(self.filter_data_tree[selected_value], option)]

        self.load_display()

    def clear_treeview(self):
        """Hủy bỏ toàn bộ Treeview cũ và thanh cuộn."""
        # Xóa Treeview cũ
        if hasattr(self, 'tree'):
            self.tree.destroy()

        # Xóa thanh cuộn
        if hasattr(self, 'v_scrollbar'):
            self.v_scrollbar.destroy()

        # Xóa tham chiếu đối tượng
        del self.tree
        del self.v_scrollbar

    def restore_data_root(self):
        """"Trả về dữ liệu ban đầu."""
        self.filter_data_tree = self.data_root
        self.current_page = 0
        self.load_display()


class TreeViewTable(BaseTreeView):
    def __init__(self, frame):
        super().__init__(frame)

        # tạo các nút phân trang
        self.next_button = ttk.Button(frame, text="Next", command=self.next_page)
        self.next_button.place(x=950, y=427)

        self.pre_button = ttk.Button(self.frame, text="Previous", command=self.prev_page)
        self.pre_button.place(x=0, y=427)

    def next_page(self):
        """Chuyển sang trang tiếp theo."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_display()

    def prev_page(self):
        """Chuyển về trang trước."""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_display()


class TreeViewFilter(BaseTreeView):
    def __init__(self, frame):
        super().__init__(frame, excluded_columns=['Date_reported', 'Country_code'],
                         filter_condition=self.filter_condition)

    def filter_condition(self, data):
        return data['Date_reported'] == '2020-01-05'
