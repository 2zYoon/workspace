# gui version toolkit
import tkinter as tk
import tkinter.ttk

w = tk.Tk()
w.title("My toolkit")
w.geometry("400x400")
w.resizable(False, False)

# menu
menu = tk.Menu(w)
menu_1 = tk.Menu(menu, tearoff=0)
menu_1.add_command(label="cmd1")
menu_1.add_command(label="cmd2")
menu.add_cascade(label="menu-1", menu=menu_1)
w.config(menu=menu)

# tabs
notebook = tkinter.ttk.Notebook(w, width=400, height=400)
notebook.pack()

tab1 = tk.Frame(w)
notebook.add(tab1, text="tab 1")
tab2 = tk.Frame(w)
notebook.add(tab2, text="tab 2")

w.mainloop()