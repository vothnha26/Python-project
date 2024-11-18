from modules import visualization as vs

if __name__ == "__main__":
    vs.create_db()  # Tạo cơ sở dữ liệu và bảng nếu chưa tồn tại
    root = vs.tk.Tk()
    app = vs.App(root, "./data/data.csv")
    root.mainloop()
