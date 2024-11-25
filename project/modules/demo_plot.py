import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, ScalarFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from modules.ClassDesign import DataAnalyzer


class ChartPlotter():
    def __init__(self):
        self.data = DataAnalyzer().data

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

            # Thêm một mục "OTHER" cho các quốc gia có tỉ lệ < 2%
            cases_by_country = pd.concat([cases_by_country, pd.Series(other_cases, index=["OTHER"])])
            percentages = pd.concat([percentages, pd.Series(100 - percentages.sum(), index=["OTHER"])])

            # Tạo biểu đồ tròn
            fig, ax = plt.subplots(figsize=(5, 6))

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
            df = self.data
            if df.empty:
                messagebox.showerror("Lỗi", "Tệp CSV không chứa dữ liệu.")
                return
            # Kiểm tra sự tồn tại của cột cần thiết
            if 'Country' not in df.columns or 'New_deaths' not in df.columns or 'Date_reported' not in df.columns:
                messagebox.showerror("Lỗi", "Tệp CSV không chứa các cột cần thiết: 'Country', 'New_deaths' hoặc 'Date_reported'.")
                return

            # Định dạng cột ngày
            df['Date_reported'] = pd.to_datetime(df['Date_reported'], format='%Y-%m-%d', errors='coerce')

            # Loại bỏ các hàng có giá trị tử vong bị thiếu
            df = df.dropna(subset=['New_deaths'])

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
    

    # def plot_chart(self, master_frame):
    #     try:
    #         # Đọc dữ liệu từ tệp CSV
    #         df = pd.read_csv(self.data_path)
    #         if df.empty:
    #             messagebox.showerror("Lỗi", "Tệp CSV không chứa dữ liệu.")
    #             return

    #         # Kiểm tra sự tồn tại của cột cần thiết
    #         if 'Country' not in df.columns or 'New_deaths' not in df.columns or 'Date_reported' not in df.columns:
    #             messagebox.showerror("Lỗi", "Tệp CSV không chứa các cột cần thiết: 'Country', 'New_deaths' hoặc 'Date_reported'.")
    #             return

    #         # Định dạng cột ngày
    #         df['Date_reported'] = pd.to_datetime(df['Date_reported'], format='%Y-%m-%d', errors='coerce')

    #         # Loại bỏ các hàng có giá trị tử vong bị thiếu
    #         df = df.dropna(subset=['New_deaths'])

    #         # Tính tổng số ca tử vong theo quốc gia
    #         deaths_by_country = df.groupby('Country')['New_deaths'].sum()

    #         # Lấy 5 quốc gia có số ca tử vong cao nhất
    #         top_5_countries = deaths_by_country.nlargest(5).index

    #         # Lọc dữ liệu chỉ chứa top 5 quốc gia
    #         top_5_data = df[df['Country'].isin(top_5_countries)]

    #         # Nhóm dữ liệu theo quốc gia và ngày
    #         grouped_data = top_5_data.groupby(['Country', 'Date_reported'])['New_deaths'].sum().reset_index()

    #         # Vẽ biểu đồ đường
    #         fig, ax = plt.subplots(figsize=(12, 6))
    #         for country in top_5_countries:
    #             country_data = grouped_data[grouped_data['Country'] == country]
    #             ax.plot(
    #                 country_data['Date_reported'],
    #                 country_data['New_deaths'],
    #                 label=country,
    #                 marker='o',
    #                 markersize=4,
    #                 alpha=0.8
    #             )

    #         # Định dạng biểu đồ
    #         ax.set_title("Top 5 Quốc Gia Có Số Ca Tử Vong Cao Nhất Theo Thời Gian", fontsize=16)
    #         ax.set_xlabel("Ngày Báo Cáo", fontsize=12)
    #         ax.set_ylabel("Số Ca Tử Vong", fontsize=12)
    #         ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Hiển thị tháng cách nhau 2
    #         ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    #         ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
    #         plt.xticks(rotation=45, ha='right')
    #         ax.legend(title="Quốc Gia", loc='upper left', fontsize=10)
    #         plt.grid(alpha=0.3)

    #         # Điều chỉnh bố cục
    #         plt.tight_layout()

    #         # Nhúng biểu đồ vào Tkinter
    #         canvas = FigureCanvasTkAgg(fig, master=master_frame)
    #         canvas.draw()
    #         canvas.get_tk_widget().pack(expand=True, fill='both')

    #     except FileNotFoundError:
    #         messagebox.showerror("Lỗi", "Không tìm thấy tệp dữ liệu. Vui lòng kiểm tra đường dẫn tệp.")
    #     except pd.errors.ParserError:
    #         messagebox.showerror("Lỗi", "Lỗi khi phân tích tệp CSV. Vui lòng kiểm tra dữ liệu.")
    #     except Exception as e:
    #         messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
