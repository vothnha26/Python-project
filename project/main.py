from modules import data_cleaning
from pathlib import Path

file_in = Path(__file__).resolve().parent.parent / 'project' / 'data' / 'data.csv'
file_out = Path(__file__).resolve().parent.parent / 'project' / 'data' / 'data_clean.csv'
data_cleaning.clean_data(file_in, file_out)

from modules import visualization as vs

if __name__ == "__main__":
    root = vs.tk.Tk()
    app = vs.App(root, file_out)
    root.mainloop()
    