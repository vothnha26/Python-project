import pandas as pd
import numpy as np

def clean_data(input_file, output_file):
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(input_file, encoding="utf-8-sig")
    print(df.isnull().sum())
    # Xử lý dữ liệu
    df["New_cases"] = df["New_cases"].fillna(0).astype(int)
    df["New_deaths"] = df["New_deaths"].fillna(0).astype(int)
    df["Cumulative_cases"] = df["Cumulative_cases"].fillna(0).astype(int)
    df["Cumulative_deaths"] = df["Cumulative_deaths"].fillna(0).astype(int)
    df["New_cases"] = np.where(df["New_cases"] < 0, 0, df["New_cases"])
    # Sửa lỗi ký tự đặc biệt
    replacements = {
        "C�te d'Ivoire": "Côte d'Ivoire",
        "Cura�ao": "Curaçao",
        "R�union": "Réunion",
        "T�rkiye": "Türkiye",
        "Barth�lemy": "Barthélemy",
    }
    df.replace(replacements, inplace=True)

    # Xóa các dòng có cột WHO_region trống
    df = df.dropna(subset=["WHO_region"])
    df = df.dropna(subset=["Cumulative_deaths"])
    df = df.dropna(subset=["Cumulative_cases"])
    # Lưu file đã làm sạch
    df.to_csv(output_file, index=False)
