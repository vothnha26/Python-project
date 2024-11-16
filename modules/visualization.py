import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import pandas as pd
from demo_plot import ChartPlotter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_db():
    conn = sqlite3.connect('data_analyze.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, username TEXT, amount REAL, description TEXT)''')
    conn.commit()
    conn.close()

def create_data_popup():
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

    # Hàm xử lý khi nhấn nút lưu
    def save_data():
        country = country_entry.get()
        cases = cases_entry.get()
        deaths = deaths_entry.get()
        messagebox.showinfo("Thêm thành công ! ")
    # Nút lưu dữ liệu

    save_button = tk.Button(popup, text="Lưu", command=save_data, bg="#00796b", fg="white", font=("Helvetica", 12))
    save_button.pack(pady=10)
    
def create_data():
    messagebox.showinfo("Create", "Function to create data")

def update_data():
    messagebox.showinfo("Update", "Function to update data")

def delete_data():
    messagebox.showinfo("Delete", "Function to delete data")

def sort_data():
    messagebox.showinfo("Sort", "Function to sort data")

def search_data():
    messagebox.showinfo("Search", "Function to search data")
class App:
    def __init__(self, master,data_path = "Python-project/project/data/WHO-COVID-19-global-data.csv"):
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
        style.map("RoundedButton.TButton", background=[('active', '#005f4f')], foreground=[('active', '#ffffff')],
                  relief=[('pressed', 'solid')])

        button_options = {'style': "RoundedButton.TButton", 'width': 25, 'padding': 10}

        self.create_button = ttk.Button(self.button_frame, text="Tạo dữ liệu mới", command=create_data_popup,
                                        **button_options)
        self.create_button.pack(pady=5)

        self.update_button = ttk.Button(self.button_frame, text="Cập nhật dữ liệu", command=update_data, **button_options)
        self.update_button.pack(pady=5)

        self.delete_button = ttk.Button(self.button_frame, text="Xóa dữ liệu", command=delete_data, **button_options)
        self.delete_button.pack(pady=5)

        self.sort_button = ttk.Button(self.button_frame, text="Sắp xếp dữ liệu", command=sort_data, **button_options)
        self.sort_button.pack(pady=5)

        self.search_button = ttk.Button(self.button_frame, text="Tìm dữ liệu", command=search_data, **button_options)
        self.search_button.pack(pady=5)

        self.chart_label = tk.Label(self.button_frame, text="Các biểu đồ thống kê", font=("Helvetica", 16, "bold"),
                                    bg="#ffffff", fg="black")
        self.chart_label.pack(pady=20)

        self.display_frame = tk.Frame(self.main_frame, bg="#ffffff", padx=20, pady=20)
        self.display_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        self.display_label = tk.Label(self.display_frame, text="Khu vực hiển thị dữ liệu", font=("Helvetica", 12),
                                      bg="#ffffff", fg="black")
        self.display_label.pack(pady=10)

        # Input và nút vẽ biểu đồ
        self.input_country = tk.Entry(self.display_frame, width=30)
        self.input_country.pack(pady=5)
        self.plot_button = ttk.Button(self.display_frame, text="Vẽ biểu đồ", command=self.display_chart)
        self.plot_button.pack(pady=5)

        self.reset_button = ttk.Button(self.display_frame, text="Reset", command=self.reset_chart)
        self.reset_button.pack(pady=5)

    def display_chart(self):
        country = self.input_country.get()
        if country:
            for widget in self.display_frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg): # Chỉ xóa canvas của biểu đồ
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
if __name__ == "__main__":
    create_db()  # Tạo cơ sở dữ liệu và bảng nếu chưa tồn tại
    root = tk.Tk()
    app = App(root)
    root.mainloop()
