import tkinter as tk
from tkinter import messagebox, ttk
from modules.treeview_table import TreeViewTable, TreeViewFilter
from modules.demo_plot import ChartPlotter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modules.crud import CRUD
from tkcalendar import Calendar


class App:
    def __init__(self, master, data_path):
        self.master = master
        master.title("Project")
        master.geometry("800x500")
        master.configure(bg="#d1f0f7")
        self.data_path = data_path

        self.title_label = tk.Label(master, text="Bảng phân tích dữ liệu số ca nhiễm COVID trên toàn thế giới",
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

        self.button_frame = tk.Frame(self.main_frame, bg="#ffffff", padx=20, pady=20)
        self.button_frame.pack(side="left", padx=10, pady=10, fill="y")

        self.subtitle_label = tk.Label(self.button_frame, text="Bảng chức năng", font=("Helvetica", 16, "bold"),
                                       bg="#ffffff", fg="black")
        self.subtitle_label.pack(pady=10)

        style = ttk.Style()
        style.configure("RoundedButton.TButton", font=("Helvetica", 12), padding=10, relief="flat",
                        background="#00796b", foreground="black")
        style.map("RoundedButton.TButton", background=[('active', 'red')], foreground=[('active', 'purple')],
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

        self.search_button = ttk.Button(self.button_frame, text="Tìm dữ liệu", **button_options,
                                        command=self.display_search_table)
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

        # TEST ------------------------------------------------
        self.treeview_table = TreeViewTable(self.button_frame)
        self.treeview_table.display_treeview()
        self.treeview_table.update_page_label()

        self.Crud_config = CRUD(data_path)

        def create_command():
            self.Crud_config.create_data_popup(self.treeview_table)

        self.create_button.configure(command=create_command)

        self.b1 = tk.Button(self.button_frame, text="A", command=self.show_tree_view_all)
        self.b1.place(x=20, y=20)
        self.b2 = tk.Button(self.button_frame, text="B", command=self.show_tree_view_filter)
        self.b2.place(x=20, y=40)

        self.cal = Calendar(self.button_frame, selectmode="day", year=2020, month=1, day=5)
        self.cal.bind("<<CalendarSelected>>", self.show_tree_view_filter)

        # END TEST -----------------------------------------------

        # Input và nút vẽ biểu đồ
        self.input_country = tk.Entry(self.display_frame, width=30)
        self.input_country.pack(pady=5)
        self.plot_button = ttk.Button(self.display_frame, text="Vẽ biểu đồ", command=self.display_chart)
        self.plot_button.pack(pady=5)

        self.reset_button = ttk.Button(self.display_frame, text="Reset", command=self.reset_chart)
        self.reset_button.pack(pady=5)

        # Tạo combobox và sự kiện 'select' cho combobox
        self.choice = ttk.Combobox(self.button_frame, width=27, state="readonly")
        self.choice['values'] = ('WHO_region', 'Cumulative_cases')
        self.choice.place(x=30, y=100)
        self.choice.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # Từ điển lưu các trạng thái của Checkbutton
        self.choices_map = {
            "WHO_region": ["EURO", "OTHER", "EMRO"],
            "Cumulative_cases": ["1000-2000", "2000-3000"]
        }
        self.checkbox_states = {}
        self.check_vars = {}
        self.check_buttons = {}

    # Hiển thị toàn bộ dữ liệu TreeView
    def show_tree_view_all(self):
        # Ẩn calendar
        self.cal.place_forget()
        self.treeview_table.clear_treeview()
        # Thêm TreeView
        self.treeview_table = TreeViewTable(self.button_frame)
        self.treeview_table.display_treeview()
        self.treeview_table.update_page_label()

    # Hiển thị dữ liệu đã lọc theo ngày
    def show_tree_view_filter(self, event=None):
        self.cal.place(x=100, y=200)
        # Thêm TreeView
        self.treeview_table.clear_treeview()

        # Tách tháng, ngày, năm
        month, day, year = map(str, self.cal.get_date().split("/"))
        year = int(year)
        # Chuẩn hóa năm (thêm 2000)
        year += 2000 if year < 100 else 0
        if len(month) == 1: month = '0' + month
        if len(day) == 1: day = '0' + day

        self.treeview_table = TreeViewFilter(self.button_frame, f"{year}-{month}-{day}")
        self.treeview_table.display_treeview()
        self.treeview_table.update_page_label()

    def remove_all_checkbuttons(self):
        """Xóa tất cả Checkbutton hiện có."""
        for key in list(self.check_buttons.keys()):
            self.check_buttons[key].destroy()
        self.checkbox_states.clear()
        self.check_vars.clear()
        self.check_buttons.clear()

    def update_checkbuttons_based_on_choice(self):
        """Tạo Checkbutton mới dựa trên danh sách options."""
        self.remove_all_checkbuttons()
        start_y = 126
        spacing = 30

        for i, option in enumerate(self.choices_map[self.choice.get()]):
            var = tk.BooleanVar()
            self.check_vars[option] = var

            # Tạo Checkbutton
            chk = tk.Checkbutton(self.button_frame, text=option, variable=var)
            chk.place(x=30, y=start_y + i * spacing)
            self.check_buttons[option] = chk
        self.checkbox_states[self.choice.get()] = self.check_vars

    def update_radiobuttons_based_on_choice(self):
        """Tạo Checkbutton mới dựa trên danh sách options."""
        self.remove_all_checkbuttons()
        start_y = 126
        spacing = 30

        for i, option in enumerate(self.choices_map[self.choice.get()]):
            var = tk.BooleanVar()
            self.check_vars[option] = var

            # Tạo Checkbutton
            chk = tk.Radiobutton(self.button_frame, text=option, variable=var)
            chk.place(x=30, y=start_y + i * spacing)
            self.check_buttons[option] = chk
        self.checkbox_states[self.choice.get()] = self.check_vars

    def on_combobox_select(self, event):
        """Xử lý sự kiện combobox."""
        selected_value = self.choice.get()
        if selected_value == "WHO_region":
            self.update_checkbuttons_based_on_choice()
        else:
            self.update_radiobuttons_based_on_choice()

    # Hiển thị bảng sau khi sắp xếp
    def display_sort_table(self):
        self.treeview_table.sort_all_data(self.sort_status)
        self.sort_status = not self.sort_status

    def display_search_table(self):
        self.treeview_table.create_search()

    # Hiển thị bảng sau khi lọc dữ liệu
    def display_filter_table(self):
        selected_value = self.choice.get()
        results = [option for option, var in self.checkbox_states[selected_value].items() if var.get() is True]
        self.treeview_table.filter_tree(selected_value, results)

    def display_chart(self):
        country = self.input_country.get()
        if country:
            for widget in self.display_frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):  # Chỉ xóa canvas của biểu đồ
                    widget.get_tk_widget().destroy()
            # Vẽ biểu đồ dựa trên tên quốc gia được nhập
            ChartPlotter.plot_chart(self, self.display_frame, country)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên quốc gia.")

    def reset_chart(self):
        # Xóa tất cả các widget liên quan đến biểu đồ khỏi display_frame
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        # Thêm lại input và nút vẽ biểu đồ
        self.display_label = tk.Label(self.display_frame, text="Khu vực hiển thị dữ liệu", font=("Helvetica", 12),
                                      bg="#ffffff", fg="black")
        self.display_label.pack(pady=10)

        self.input_country = tk.Entry(self.display_frame, width=30)
        self.input_country.pack(pady=5)

        self.plot_button = ttk.Button(self.display_frame, text="Vẽ biểu đồ", command=self.display_chart)
        self.plot_button.pack(pady=5)

        self.reset_button = ttk.Button(self.display_frame, text="Reset", command=self.reset_chart)
        self.reset_button.pack(pady=5)
