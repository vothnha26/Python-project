from tkinter import ttk
from ClassDesign import DataAnalyzer

# Số lượng dòng hiển thị mỗi trang
ROWS_PER_PAGE = 1000


class TreeViewTable:
    def __init__(self, data_path, frame):
        self.frame = frame
        self.tree = ttk.Treeview(self.frame, selectmode="extended")
        self.data_tree = DataAnalyzer(data_path)
        self.tree["columns"] = ["No."] + list(self.data_tree.data.columns)
        self.tree["show"] = "headings"

        self.tree.heading("No.", text="No.")
        self.tree.column("No.", width=50, anchor='center')
        for col in self.data_tree.data.columns:
            self.tree.heading(col, text=col)
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

        self.pre_button = ttk.Button(self.frame, text="Previous", command=self.prev_page)
        self.pre_button.place(x=0, y=375)

        self.page_label = ttk.Label(frame, text="")
        self.page_label.pack()

        # Các biến để quản lý phân trang và sắp xếp
        self.current_page = 0
        self.total_pages = len(self.data_tree.data) // ROWS_PER_PAGE + (
            1 if len(self.data_tree.data) % ROWS_PER_PAGE != 0 else 0)

    def display_data(self, page):
        """Hiển thị dữ liệu lên Treeview theo trang, bao gồm cột thứ tự."""
        self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ
        start = page * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE
        print(page)
        for i, (_, row) in enumerate(self.data_tree.data.iloc[start:end].iterrows(), start=1):
            self.tree.insert("", "end", values=[start + i] + list(row))

    def next_page(self):
        """Chuyển sang trang tiếp theo."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_data(self.current_page)
            self.update_page_label()

    def prev_page(self):
        """Chuyển về trang trước."""
        if self.current_page > 0:
            self.current_page -= 1
            self.display_data(self.current_page)
            self.update_page_label()

    def update_page_label(self):
        """Cập nhật nhãn hiển thị số trang."""
        self.page_label.config(text=f"Page {self.current_page + 1} of {self.total_pages}")
