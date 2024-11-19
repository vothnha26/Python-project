from modules import visualization as vs

if __name__ == "__main__":
    root = vs.tk.Tk()
    app = vs.App(root, "./data/data.csv")
    root.mainloop()
