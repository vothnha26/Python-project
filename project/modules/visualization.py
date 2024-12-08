import tkinter as tk
from calendar import Calendar
from tkinter import messagebox, ttk
from tkinter import *
from modules.ClassDesign import DataAnalyzer
from modules.treeview_task import TreeViewTable
from modules.demo_plot import ChartPlotter
from modules.crud import CRUD
from tkcalendar import Calendar


class App:
    def __init__(self, master, data_path):
        self.master = master
        master.title("Project")
        master.geometry("3000x900")
        master.configure(bg="#d1f0f7")
        self.data_path = data_path

        self.title_label = tk.Label(master, text="BẢNG THỐNG KÊ DỮ LIỆU SỐ CA NHIỄM COVID TRÊN TOÀN THẾ GIỚI",
                                    font=("Helvetica", 14, "bold"), bg="#d1f0f7", fg="black")
        self.title_label.pack(pady=10)

        self.main_frame = tk.Frame(master, bg="#d1f0f7")
        self.main_frame.pack(expand=True, fill='both')

        self.canvas = tk.Canvas(self.main_frame, bg="#ffffff", borderwidth=0, highlightthickness=0)

        self.button_frame = tk.Frame(self.canvas, bg="#ffffff")

        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.button_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.button_frame = tk.Frame(self.main_frame, bg="#ffffff", width=700, padx=20, pady=20)
        self.button_frame.pack_propagate(False)  # Ngăn button_frame thay đổi kích thước theo nội dung
        self.button_frame.pack(side="left", padx=10, pady=10, fill="y")

        self.subtitle_label = tk.Label(self.button_frame, text="Bảng chức năng", font=("Helvetica", 16, "bold"),
                                       bg="#ffffff", fg="black")
        self.subtitle_label.pack(pady=10)

        style = ttk.Style()
        style.configure("RoundedButton.TButton", font=("Helvetica", 12), padding=10, relief="flat",
                        background="#00796b", foreground="black")
        style.map("RoundedButton.TButton", background=[('active', '#005f4f')], foreground=[('active', '#ffffff')],
                  relief=[('pressed', 'solid')])

        button_options = {'style': "RoundedButton.TButton", 'width': 25, 'padding': 10}

        self.create_button = ttk.Button(self.button_frame, text="Tạo dữ liệu mới",
                                        **button_options)
        self.create_button.pack(pady=5)

        self.update_button = ttk.Button(self.button_frame, text="Cập nhật dữ liệu",
                                        **button_options)
        self.update_button.pack(pady=5)

        self.delete_button = ttk.Button(self.button_frame, text="Xóa dữ liệu", **button_options)
        self.delete_button.pack(pady=5)

        self.sort_button = ttk.Button(self.button_frame, text="Sắp xếp dữ liệu", command=self.display_sort_table,
                                      **button_options)
        self.sort_status = True
        self.sort_button.pack(pady=5)

        self.search_button = ttk.Button(self.button_frame, text="Tìm dữ liệu", **button_options)
        self.search_button.pack(pady=5)

        self.filter_button = ttk.Button(self.button_frame, text="Lọc dữ liệu", command=self.display_filter_table,
                                        **button_options)
        self.filter_button.pack(pady=5)

        self.chart_label = tk.Label(self.button_frame, text="Bảng số liệu", font=("Helvetica", 16, "bold"),
                                    bg="#ffffff", fg="black")
        self.chart_label.pack(pady=20)

        self.display_frame = tk.Frame(self.main_frame, bg="#ffffff", padx=20, pady=20)
        self.display_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        self.display_label = tk.Label(self.display_frame, text="Khu vực hiển thị dữ liệu", font=("Helvetica", 12),
                                      bg="#ffffff", fg="black")
        self.display_label.pack(pady=10)

        self.treeview_table = TreeViewTable(self.button_frame)
        self.treeview_table.display_treeview()
        self.treeview_table.update_page_label()

        entry = Entry(self.button_frame)
        entry.place(x=455, y=427)

        def to_page(event):
            try:
                page = int(entry.get())
                if 0 < page <= self.treeview_table.total_pages:
                    self.treeview_table.current_page = page - 1 if entry.get() != '' else 0
                    self.treeview_table.display_treeview()
                else:
                    messagebox.showinfo("Lỗi", "Vui lòng nhập lại")
            except Exception as e:
                messagebox.showerror("Lỗi", f"{e}")

        entry.bind("<Return>", to_page)

        def search_command():
            popup = tk.Toplevel()
            popup.title("Tìm kiếm")
            popup.geometry("300x400")
            popup.configure(bg="#f0f0f0")

            # Tiêu đề
            title_label = tk.Label(popup, text="Tìm kiếm", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
            title_label.pack(pady=10)

            date_label = tk.Label(popup, text="Ngày tháng năm (YYYY-MM-DD):", bg="#f0f0f0")
            date_label.pack(pady=5)
            date_entry = tk.Entry(popup, width=30)
            date_entry.pack(pady=5)

            country_label = tk.Label(popup, text="Tên nước:", bg="#f0f0f0")
            country_label.pack(pady=5)
            country_entry = tk.Entry(popup, width=30)
            country_entry.pack(pady=5)

            # Nút lưu dữ liệu
            find_button = tk.Button(popup, text="Tìm kiếm",
                                    command=lambda: self.treeview_table.search_country_tree(country_entry.get(),
                                                                                            date_entry.get()),
                                    bg="#00796b", fg="white", font=("Helvetica", 12))
            find_button.pack(pady=10)
            date_ex_label = tk.Label(popup,text="EX: 2020-01-05",font=("Helvetica", 14))
            date_ex_label.pack()

        self.search_button.configure(command=search_command)

        self.Crud_config = CRUD()

        def create_command():
            self.Crud_config.create_data_popup(self.treeview_table)

        self.create_button.configure(command=create_command)

        def update_command():
            self.Crud_config.update_data_popup(self.treeview_table)

        self.update_button.configure(command=update_command)

        def delete_command():
            self.Crud_config.delete_multiple_data(self.treeview_table)

        self.delete_button.configure(command=delete_command)

        self.b1 = tk.Button(self.button_frame, text="Dữ liệu tệp", command=self.show_tree_view_all)
        self.b1.place(x=20, y=20)
        self.b2 = tk.Button(self.button_frame, text="Dữ liệu theo ngày", command=self.show_tree_view_filter)
        self.b2.place(x=20, y=40)

        self.cal = Calendar(self.main_frame, selectmode="day", year=2020, month=1, day=5)
        self.cal.bind("<<CalendarSelected>>", self.show_tree_view_filter)

        # Input và nút vẽ biểu đồ

        self.input_country = tk.Entry(self.display_frame, width=30)
        self.input_country.pack(pady=5)
        # Combobox
        self.chart_type_label = tk.Label(self.display_frame, text="Chọn kiểu biểu đồ", font=("Helvetica", 12),
                                         bg="#ffffff")
        self.chart_type_label.pack(pady=10)

        self.chart_type_combobox = ttk.Combobox(self.display_frame, values=["Biểu đồ cột về số ca mắc mới",
                                                                            "Biểu đồ tròn về số ca tử vong mới",
                                                                            "Biểu đồ đường về top 5 quốc gia có nhiều ca tử vong nhất",
                                                                            "Biểu đồ cột về số ca đã/ đang điều trị",
                                                                            "Số ca tử vong tích lũy"],
                                                state="readonly", width=50)
        self.chart_type_combobox.pack(pady=5)

        self.plot_button = ttk.Button(self.display_frame, text="Vẽ biểu đồ", command=self.chart_selection)
        self.plot_button.pack(pady=5)

        self.reset_button = ttk.Button(self.display_frame, text="Reset", command=self.reset_chart)
        self.reset_button.pack(pady=5)

    # Hiển thị toàn bộ dữ liệu TreeView
    def show_tree_view_all(self):
        self.cal.place_forget()

        # Cập nhật trạng thái bảng
        self.treeview_table.cal_status = False
        self.treeview_table.filter_data_tree = DataAnalyzer().data
        self.treeview_table.display_treeview()
        self.treeview_table.update_page_label()

    # Hiển thị dữ liệu đã lọc theo ngày
    def show_tree_view_filter(self, event=None):
        self.cal.place(x=600, y=50)
        # Tách tháng, ngày, năm
        month, day, year = map(str, self.cal.get_date().split("/"))
        year = int(year)
        # Chuẩn hóa năm (thêm 2000)
        year += 2000 if year < 100 else 0
        if len(month) == 1: month = '0' + month
        if len(day) == 1: day = '0' + day

        # Cập nhật ngày, dữ liệu của bảng
        date = f"{year}-{month}-{day}"
        self.treeview_table.cal_status = True
        self.treeview_table.date = date
        self.treeview_table.filter_data_tree = DataAnalyzer().filter_data_root(date)
        self.treeview_table.display_treeview()

    # Hiển thị bảng sau khi sắp xếp
    def display_sort_table(self):
        self.treeview_table.sort_all_data(self.sort_status)
        self.sort_status = not self.sort_status

    # Hiển thị bảng sau khi lọc dữ liệu
    def display_filter_table(self):

        popup = tk.Toplevel()
        popup.title("Lọc dữ liệu")

        # Tiêu đề
        options_area = ['AMRO', 'WPRO', 'EURO', 'SEARO', 'AFRO', 'EMRO', 'OTHER']
        options_year = ['2020', '2021', '2022', '2023', '2024']

        Label(popup, text="Khu vực", bg="#00796b", fg="white", font=("Helvetica", 16)).grid(row=0, columnspan=7)

        # Danh sách lưu trạng thái của các checkbutton
        filter_area = {}
        filter_year = {}

        for i, option in enumerate(options_area):
            var = tk.BooleanVar()
            Checkbutton(popup, text=option, variable=var).grid(row=1, column=i)
            filter_area[option] = var

        if self.treeview_table.cal_status is False:
            Label(popup, text="Năm", bg="#00796b", fg="white", font=("Helvetica", 16)).grid(row=2, columnspan=7)

            for i, option in enumerate(options_year):
                var = tk.BooleanVar()
                Checkbutton(popup, text=option, variable=var).grid(row=3, column=i + 1)
                filter_year[option] = var

        # Nút lọc dữ liệu
        filter_button = tk.Button(popup, text="Lọc dữ liệu",
                                  command=lambda: self.treeview_table.filter_tree(filter_area, filter_year),
                                  bg="#00796b", fg="white", font=("Helvetica", 12))
        filter_button.grid(row=4, columnspan=7, pady=10)

    def chart_selection(self):
        chart_type = self.chart_type_combobox.get()  # Lấy giá trị từ Combobox
        country = self.input_country.get().strip()

        if not chart_type:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn kiểu biểu đồ.")
            return
        if not country and chart_type != "Biểu đồ tròn về số ca tử vong mới" and chart_type != "Biểu đồ đường về top 5 quốc gia có nhiều ca tử vong nhất" and chart_type != "Biểu đồ cột về số ca đã/ đang điều trị" and chart_type != "Số ca tử vong tích lũy":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên quốc gia.")
            return

        # Chuẩn hóa tên quốc gia
        country = " ".join([word.capitalize() for word in country.split()])

        chart = ChartPlotter(self.treeview_table.filter_data_tree)
        if chart_type == "Biểu đồ cột về số ca mắc mới":
            chart.bar_chart(self.display_frame, country)
        elif chart_type == "Biểu đồ tròn về số ca tử vong mới":
            chart.pie_chart(self.display_frame)
        elif chart_type == "Biểu đồ đường về top 5 quốc gia có nhiều ca tử vong nhất":
            chart.plot_chart(self.display_frame)
        elif chart_type == "Biểu đồ cột về số ca đã/ đang điều trị":
            chart.plot_total_recovery(self.display_frame)
        elif chart_type == "Số ca tử vong tích lũy":
            chart.line_chart(self.display_frame)

    def reset_chart(self):

        # Xóa tất cả các widget liên quan đến biểu đồ khỏi display_frame
        for widget in self.display_frame.winfo_children():
            if widget == self.cal:
                continue
            widget.destroy()
        # Thêm lại input và nút vẽ biểu đồ
        self.display_label = tk.Label(self.display_frame, text="Khu vực hiển thị dữ liệu", font=("Helvetica", 12),
                                      bg="#ffffff", fg="black")
        self.display_label.pack(pady=10)

        self.input_country = tk.Entry(self.display_frame, width=30)
        self.input_country.pack(pady=5)

        # combobox
        self.chart_type_label = tk.Label(self.display_frame, text="Chọn kiểu biểu đồ", font=("Helvetica", 12),
                                         bg="#ffffff")
        self.chart_type_label.pack(pady=10)

        self.chart_type_combobox = ttk.Combobox(self.display_frame, values=["Biểu đồ cột về số ca mắc mới",
                                                                            "Biểu đồ tròn về số ca tử vong mới",
                                                                            "Biểu đồ đường về top 5 quốc gia có nhiều ca tử vong nhất",
                                                                            "Biểu đồ cột về số ca đã/ đang điều trị",
                                                                            "Số ca tử vong tích lũy"],
                                                state="readonly", width=50)
        self.chart_type_combobox.pack(pady=5)

        self.plot_button = ttk.Button(self.display_frame, text="Vẽ biểu đồ", command=self.chart_selection)
        self.plot_button.pack(pady=5)

        self.reset_button = ttk.Button(self.display_frame, text="Reset", command=self.reset_chart)
        self.reset_button.pack(pady=5)
