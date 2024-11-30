from modules import data_cleaning

file_in = './data/data.csv'
file_out = './data/data_clean.csv'
data_cleaning.clean_data(file_in, file_out)

from modules import visualization as vs

if __name__ == "__main__":
    root = vs.tk.Tk()
    app = vs.App(root, file_out)
    root.mainloop()
    