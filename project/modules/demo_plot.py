import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, ScalarFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

class ChartPlotter:
    def __init__(self, data_path = "Python-project/project/data/WHO-COVID-19-global-data.csv"):
        # Đường dẫn đến tệp CSV
        self.data_path = data_path

    def plot_chart(self, master_frame, country):
        try:    
            df = pd.read_csv(self.data_path)
            if df.empty:
                messagebox.showerror("Lỗi", "Tệp CSV không chứa dữ liệu.")
                return
            df['Date_reported'] = pd.to_datetime(
                df['Date_reported'],
                format='%Y-%m-%d',
                errors='coerce'
            )

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
