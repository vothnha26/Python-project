import copy
from tkinter import ttk
import tkinter as tk
from modules.ClassDesign import DataAnalyzer

# Số lượng dòng hiển thị mỗi trang
ROWS_PER_PAGE = 1000


class TreeViewTable:
    def __init__(self, data_path, frame):
        self.frame = frame
        self.tree = ttk.Treeview(self.frame, selectmode="extended")
        self.data_tree = DataAnalyzer(data_path)
        self.filter_data_tree = copy.deepcopy(self.data_tree)
        self.tree["columns"] = ["No."] + list(self.filter_data_tree.data.columns)
        self.tree["show"] = "headings"

        # Tạo tiêu đề cho các cột
        self.tree.heading("No.", text="No.")
        self.tree.column("No.", width=50, anchor='center')
        for col in self.filter_data_tree.data.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c, True))
            self.tree.column(col, width=120, anchor='center')

        # Thêm thanh cuộn dọc
        self.v_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.v_scrollbar.set)
        self.v_scrollbar.pack(side='right', fill='y')

        # Đặt Treeview vào Frame
        self.tree.pack(expand=True, fill='both')

        # tạo các nút và nhãn
        self.next_button = ttk.Button(frame, text="Next", command=self.next_page)
        self.next_button.place(x=950, y=375)

        # Khởi tạo BooleanVar để theo dõi trạng thái của Checkbutton
        self.var = tk.BooleanVar()
        self.check_button = tk.Checkbutton(self.frame, command=self.filter_tree, variable=self.var)
        self.check_button.place(x=0, y=0)
        self.label1 = ttk.Label(frame, text="OTHER")
        self.label1.place(x=35, y=5)

        self.pre_button = ttk.Button(self.frame, text="Previous", command=self.prev_page)
        self.pre_button.place(x=0, y=375)

        self.page_label = ttk.Label(frame, text="")
        self.page_label.pack()

        # Các biến để quản lý phân trang
        self.current_page = 0
        self.total_pages = len(self.filter_data_tree.data) // ROWS_PER_PAGE + (
            1 if len(self.filter_data_tree.data) % ROWS_PER_PAGE != 0 else 0)

    def update_total_pages(self):
        self.total_pages = len(self.filter_data_tree.data) // ROWS_PER_PAGE + (
            1 if len(self.filter_data_tree.data) % ROWS_PER_PAGE != 0 else 0)

    def display_data(self, page):
        """Hiển thị dữ liệu lên Treeview theo trang, bao gồm cột thứ tự."""
        self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ
        start = page * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE

        for i, (_, row) in enumerate(self.filter_data_tree.data.iloc[start:end].iterrows(), start=1):
            self.tree.insert("", "end", values=[start + i] + list(row))

    def next_page(self):
        """Chuyển sang trang tiếp theo."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_total_pages()
            self.display_data(self.current_page)
            self.update_page_label()

    def prev_page(self):
        """Chuyển về trang trước."""
        if self.current_page > 0:
            self.update_total_pages()
            self.current_page -= 1
            self.display_data(self.current_page)
            self.update_page_label()

    def update_page_label(self):
        """Cập nhật nhãn hiển thị số trang."""
        self.page_label.config(text=f"Page {self.current_page + 1} of {self.total_pages}")

    def sort_treeview(self, col, descending):
        # Thử nghiệm sắp xếp dữ liệu trên bảng
        self.filter_data_tree.data = self.filter_data_tree.data.sort_values(by=col, ascending=descending)
        self.display_data(self.current_page)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not descending))

    def filter_tree(self):
        # Thử nghiệm lọc dữ liệu trên bảng
        self.filter_data_tree.data = self.filter_data_tree.data[
            self.filter_data_tree.data["WHO_region"] == "EURO"] if self.var.get() else self.data_tree.data

        self.update_total_pages()
        self.update_page_label()
        self.display_data(self.current_page)
