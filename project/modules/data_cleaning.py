from pathlib import Path
import pandas as pd
import numpy as np

# Đường dẫn tương đối đến file data.csv
file_path = Path(__file__).resolve().parent.parent / 'data' / 'data.csv'
file_new_path = Path(__file__).resolve().parent. parent / 'data' / 'data_clean.csv'

# Đọc dữ liệu từ file CSV
df=pd.read_csv(file_path,encoding="utf-8-sig")

# Làm sạch dữ liệu
df["New_cases"] = df["New_cases"].fillna(0).astype(int)
df["New_cases"] = np.where(df["New_cases"] < 0, 0, df["New_cases"])
df["New_deaths"] = df["New_deaths"].fillna(0).astype(int)
replacements = {
    "C�te d'Ivoire": "Côte d'Ivoire",
    "Cura�ao": "Curaçao",
    "R�union": "Réunion",
    "T�rkiye": "Türkiye",
    "Barth�lemy": "Barthélemy",
}
df.replace(replacements, inplace=True)

# ghi file vào file data_clean.csv
df.to_csv(file_new_path, index=False) 

print("Dữ liệu đã được lưu vào tệp data_clean.csv.")
