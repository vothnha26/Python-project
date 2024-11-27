import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, ScalarFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox



class ChartPlotter:

    def __init__(self, filter_data_tree):
        self.data = filter_data_tree

    def bar_chart(self, master_frame, country):
        try:
            df = self.data
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
            ax.set_xlabel('Ngày')
            ax.set_ylabel('Số Ca Nhiễm Mới')
            ax.set_title(f'Số Ca Nhiễm Mới Ở {country}')

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
            df = self.data
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

            if (other_cases > 0):
                # Thêm một mục "OTHER" cho các quốc gia có tỉ lệ < 2%
                cases_by_country = pd.concat([cases_by_country, pd.Series(other_cases, index=["OTHER"])])
                percentages = pd.concat([percentages, pd.Series(100 - percentages.sum(), index=["OTHER"])])
            
            # Tạo biểu đồ tròn
            fig, ax = plt.subplots(figsize=(1, 1))
            ax.set_position([0, 0.1, 0.6, 0.6])

            wedges, texts = ax.pie(
                cases_by_country,
                labels=None,  # Không thêm nhãn trực tiếp vào biểu đồ
                startangle=90,
                colors=plt.cm.tab20.colors
            )
            
            # Thêm chú thích ngoài biểu đồ
            ax.legend(
                wedges,
                [f"{country}: {percentage:.2f}% ({int(cases):,} cases)" 
                for country, percentage, cases in zip(cases_by_country.index, percentages, cases_by_country)],
                title="Quốc gia",
                loc="center left",
                bbox_to_anchor=(0.9, 0, 0.4 , 1)
            )

            # Thiết lập tiêu đề và cân bằng biểu đồ
            ax.set_title("Số ca nhiễm mới trên thế giới", fontsize=14, pad=0)
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
            df = self.data
            if df.empty:
                messagebox.showerror("Lỗi", "Tệp CSV không chứa dữ liệu.")
                return

            # Định dạng cột ngày
            df['Date_reported'] = pd.to_datetime(df['Date_reported'], format='%Y-%m-%d', errors='coerce')


            # Tính tổng số ca tử vong theo quốc gia
            deaths_by_country = df.groupby('Country')['New_deaths'].sum()

            # Lấy 5 quốc gia có số ca tử vong cao nhất
            top_5_countries = deaths_by_country.nlargest(5).index

            # Lọc dữ liệu chỉ chứa top 5 quốc gia
            top_5_data = df[df['Country'].isin(top_5_countries)]

            # Nhóm dữ liệu theo quốc gia và ngày
            grouped_data = top_5_data.groupby(['Country', 'Date_reported'])['New_deaths'].sum().reset_index()

            # Vẽ biểu đồ đường
            fig, ax = plt.subplots(figsize=(12, 6))
            for country in top_5_countries:
                country_data = grouped_data[grouped_data['Country'] == country]
                ax.plot(
                    country_data['Date_reported'],
                    country_data['New_deaths'],
                    label=country,
                    marker='o',
                    markersize=4,
                    alpha=0.8
                )

            # Định dạng biểu đồ
            ax.set_title("Top 5 Quốc Gia Có Số Ca Tử Vong Cao Nhất Theo Thời Gian", fontsize=16)
            ax.set_xlabel("Ngày Báo Cáo", fontsize=12)
            ax.set_ylabel("Số Ca Tử Vong", fontsize=12)
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Hiển thị tháng cách nhau 2
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
            plt.xticks(rotation=45, ha='right')
            ax.legend(title="Quốc Gia", loc='upper left', fontsize=10)
            plt.grid(alpha=0.3)

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
    def plot_total_recovery(self, master_frame):
        try:
            df = self.data
            df['Date_reported'] = pd.to_datetime(df['Date_reported'], format='%Y-%m-%d', errors='coerce')
            

            recovery_by_date = df.groupby('Date_reported')['Total_recovery'].sum().reset_index()
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(recovery_by_date['Date_reported'], recovery_by_date['Total_recovery'], linestyle='-', linewidth=2, markersize=4)
            
            # Định dạng biểu đồ
            ax.set_title('Tổng Số Ca Hồi Phục COVID-19', fontsize=14)
            ax.set_xlabel('Ngày', fontsize=12)
            ax.set_ylabel('Số Ca Hồi Phục', fontsize=12)
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Hiển thị tháng cách nhau 2
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
            ax.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=master_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill='both')

        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy tệp dữ liệu. Vui lòng kiểm tra đường dẫn tệp.")
        except pd.errors.ParserError:
            messagebox.showerror("Lỗi", "Lỗi khi phân tích tệp CSV. Vui lòng kiểm tra dữ liệu.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
