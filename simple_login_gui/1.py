from tkinter import *
import hashlib

class LOGIN:
    def __init__(self):
        self.main_gui = Tk()
        self.main_gui.title("LOGIN")
        self.main_gui.eval("tk::PlaceWindow . center")
        self.main_gui.geometry("300x200")
        self.main_gui.resizable(False, False)
        self.main_gui.grid_rowconfigure(0, weight=2)
        self.main_gui.grid_columnconfigure(0, weight=1)
        self.main_gui.grid_rowconfigure(1, weight=1)

        frame1 = Frame(self.main_gui)
        
        frame1.grid(row=1, column=0)
        frame1.grid_columnconfigure(0, weight=1)

        frame2 = Frame(frame1)
        frame2.grid(row=0, column=0, pady=15, sticky=EW)

        frame3 = Frame(frame1)
        frame3.grid(row=1, column=0, sticky=EW)
        frame3.grid_rowconfigure(0, weight=1)
        frame3.grid_columnconfigure(0, weight=5)
        frame3.grid_columnconfigure(1, weight=1)
        frame3.grid_columnconfigure(2, weight=5)

        Label(frame2, text="      ID", font=("Consolas", 13)).grid(row=0, column=0, padx=5)
        Label(frame2, text="PASSWORD", font=("Consolas", 13)).grid(row=1, column=0, padx=5)

        self.id_entry = Entry(frame2, width=20)
        self.pw_entry = Entry(frame2, width=20, show="*")
        self.id_entry.configure(bd=0,
                                borderwidth=1,
                                relief=SOLID,
                                font=("Consolas", 13))
        self.pw_entry.configure(bd=0,
                                borderwidth=1,
                                relief=SOLID,
                                font=("Consolas", 13))

        self.id_entry.grid(row=0, column=1)
        self.pw_entry.grid(row=1, column=1)
        self.id_entry.bind("<Return>", self.login)
        self.pw_entry.bind("<Return>", self.login)

        self.but_login = Label(frame3, text='SIGN UP', height=2)
        self.but_login.bind("<Button-1>", self.login)
        self.but_login.bind("<Enter>", self.hover_1)   
        self.but_login.bind("<Leave>", self.leave_1)    
        self.but_login.configure(background='white', 
                           borderwidth=1,
                           relief=SOLID,
                           font=("Consolas", 13))
        self.but_login.grid(row=0, column=0, sticky=EW)

        self.but_signup = Label(frame3, text='SIGN IN', height=2)
        self.but_signup.bind("<Button-1>", self.login)    
        self.but_signup.bind("<Enter>", self.hover_2)   
        self.but_signup.bind("<Leave>", self.leave_2)        
        self.but_signup.configure(background='white', 
                           borderwidth=1,
                           relief=SOLID,
                           font=("Consolas", 13))
        self.but_signup.grid(row=0, column=2, sticky=EW)

        self.id_entry.focus_set()
    

    def show(self):
        self.main_gui.mainloop()

    def hover_1(self, e):
        self.but_login.configure(foreground="white", background="black")
    def leave_1(self, e):
        self.but_login.configure(foreground="black", background="white")

    def hover_2(self, e):
        self.but_signup.configure(foreground="white", background="black")
    def leave_2(self, e):
        self.but_signup.configure(foreground="black", background="white")


    def login(self, e):
        self.real_login(str(self.id_entry.get()), str(self.pw_entry.get()))

    def real_login(self, user_id, user_pwd):
        idpwd = (user_id, str(hashlib.sha256(user_pwd.encode()).hexdigest()))
        print(idpwd)

abc = LOGIN()
abc.show()