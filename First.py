from tkinter import *
from tkinter import messagebox
import mysql.connector 
  
 
class Login:
    def __init__(self, window):
        self.window = window 

        def sign_up():
            from A1 import Register
            Register(self.window)


        self.logo = PhotoImage(file = "Images\\M.png")

        frame = Frame(self.window, background="#ffdab9")
        frame.place(x=483, y=90, width=574, height=600)
        Label(frame, image = self.logo, background = "black").place(x = 40, y = 40)
        Label(frame, text="The ", background="#ffdab9", font=("aerial", 50, "bold")).place(x=300, y=30)
        Label(frame, text="University ", background="#ffdab9", font=("aerial", 50, "bold")).place(x=215, y=100)
        Label(frame, text="Username", background="#ffdab9", font=("aerial", 30, "bold")).place(x=30, y=210)
        Label(frame, text="Password", background="#ffdab9", font=("aerial", 30, "bold")).place(x=30, y=345)

        self.username = Entry(frame, font=("aerial", 30, "bold"), background="#008080", foreground="white")
        self.username.place(x=35, y=270, height=50, width=500)

        self.password = Entry(frame, font=("aerial", 30, "bold"), background="#008080", foreground="white")
        self.password.place(x=35, y=405, height=50, width=500)

        sign_up = Button(frame, text="Sign Up", font=("aerial", 15, "bold"), command=sign_up, background="#ffdab9",
                         borderwidth=0, activebackground="#ffdab9", foreground="black")
        sign_up.place(x=30, y=540)


        login = Button(frame, text="Login", width=7, font=("aerial", 20, "bold"), command=self.login,
                       background="#008080", activebackground="#ffdab9", foreground="white", relief=RAISED, bd=10)
        login.place(x=210, y=475)




if __name__ == "__main__":
    window = Tk()
    Login(window)
    window.title("Face Recognition System")
    window.geometry("1530x800+-5+0")
    window.config(background="#008080")
    icon = PhotoImage(file = "Images\\M.png")
    window.iconphoto(True, icon)
    window.mainloop()
