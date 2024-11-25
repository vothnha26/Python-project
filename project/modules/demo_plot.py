import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, ScalarFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

class ChartPlotter():
    def __init__(self, data_path="D:/PYTHON(project)/Python-project/project/data/data_clean.csv"):
        # Đường dẫn đến tệp CSV
        self.data_path = data_path

    def bar_chart(self, master_frame, country):
        try:
            df = pd.read_csv(self.data_path)
            if df.empty:
                messagebox.showerror("Lỗi", "Tệp CSV không chứa dữ liệu.")
                return
            df['Date_reported'] = pd.to_datetime(df['Date_reported'], format='%Y-%m-%d', errors='coerce')

            # Chỉnh sửa tên quốc gia để chuẩn hóa
            country_demo = country.split()
            for i in range(len(country_demo)):
                country_demo[i] = country_demo[i].capitalize()
            country = " ".join(country_demo)

            # Lọc dữ liệu theo quốc gia và loại bỏ các giá trị 0 trong `New_cases`
            filtered_df = df[df['Country'] == country]
            filtered_df = filtered_df[filtered_df['New_cases'] != 0]

            # Thiết lập lại chỉ số sau khi lọc
            filtered_df.reset_index(drop=True, inplace=True)

            # Lọc dữ liệu theo khoảng thời gian
            start_date = '2021-10-27'
            end_date = '2023-11-01'
            filtered_time_df = filtered_df[
                (filtered_df['Date_reported'] >= start_date) & (filtered_df['Date_reported'] <= end_date)
            ]

            # Kiểm tra nếu không có dữ liệu trong khoảng thời gian chỉ định
            if filtered_time_df.empty:
                messagebox.showwarning("Không có dữ liệu", f"Không có dữ liệu cho {country} trong khoảng thời gian này.")
                return

            # Vẽ biểu đồ
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(filtered_time_df['Date_reported'], filtered_time_df['New_cases'], width=2)
            ax.set_xlabel('Date_reported')
            ax.set_ylabel('New_cases')
            ax.set_title(f'New Cases in {country}')

            # Định dạng trục x và y
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
            ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

            # Xoay nhãn và điều chỉnh bố cục
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Nhúng biểu đồ vào Tkinter
            canvas = FigureCanvasTkAgg(fig, master=master_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill='both')

        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy tệp dữ liệu. Vui lòng kiểm tra đường dẫn tệp.")
        except pd.errors.ParserError:
            messagebox.showerror("Lỗi", "Lỗi khi phân tích tệp CSV. Vui lòng kiểm tra dữ liệu.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def pie_chart(self, master_frame):
        try:
            df = pd.read_csv(self.data_path)
            if df.empty:
                messagebox.showerror("Lỗi", "Tệp CSV không chứa dữ liệu.")
                return

            # Tính tổng số ca theo quốc gia
            cases_by_country = df.groupby('Country')['New_cases'].sum()

            # Sắp xếp dữ liệu từ lớn đến nhỏ
            cases_by_country = cases_by_country.sort_values(ascending=False)

            # Tính tỉ lệ phần trăm cho từng quốc gia
            percentages = (cases_by_country / cases_by_country.sum()) * 100

            # Tính tổng số ca cho các quốc gia có tỉ lệ < 2%
            other_cases = cases_by_country[percentages < 2].sum()

            # Lọc ra các quốc gia có tỉ lệ >= 2%
            cases_by_country = cases_by_country[percentages >= 2]
            percentages = percentages[percentages >= 2]

            # Thêm một mục "OTHER" cho các quốc gia có tỉ lệ < 2%
            cases_by_country = pd.concat([cases_by_country, pd.Series(other_cases, index=["OTHER"])])
            percentages = pd.concat([percentages, pd.Series(100 - percentages.sum(), index=["OTHER"])])

            # Tạo biểu đồ tròn
            fig, ax = plt.subplots(figsize=(6, 6))

            # Vẽ biểu đồ tròn với nhãn chỉ cho các quốc gia có tỉ lệ >= 2%
            ax.pie(cases_by_country, 
                labels=[f"{country}: {percentage:.2f}% ({int(cases):,} cases)" 
                        if country != "OTHER" else f"OTHER: {percentage:.2f}% ({int(other_cases):,} cases)"
                        for country, percentage, cases in zip(cases_by_country.index, percentages, cases_by_country)],
                startangle=0,
                colors=plt.cm.tab20.colors,
                labeldistance=1.1,  
                pctdistance=0.85,   
                autopct=None,
                wedgeprops={'linewidth': 1, 'linestyle': '-'})

            # Thiết lập tiêu đề và bố cục
            ax.set_title("Số ca nhiễm mới trên thế giới", fontsize=14, pad=30)
            
            # Đảm bảo biểu đồ có dạng hình tròn
            plt.axis('equal')

            # Điều chỉnh bố cục
            plt.tight_layout()

            # Nhúng biểu đồ vào Tkinter
            canvas = FigureCanvasTkAgg(fig, master=master_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill='both')

        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy tệp dữ liệu. Vui lòng kiểm tra đường dẫn tệp.")
        except pd.errors.ParserError:
            messagebox.showerror("Lỗi", "Lỗi khi phân tích tệp CSV. Vui lòng kiểm tra dữ liệu.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
    def plot_chart(self, master_frame):
        try:
            df = pd.read_csv(self.data_path)
            if df.empty:
                messagebox.showerror("Lỗi", "Tệp CSV không chứa dữ liệu.")
                return
            


        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy tệp dữ liệu. Vui lòng kiểm tra đường dẫn tệp.")
        except pd.errors.ParserError:
            messagebox.showerror("Lỗi", "Lỗi khi phân tích tệp CSV. Vui lòng kiểm tra dữ liệu.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
    
