import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import gp_home
import patient_home
import admin_home
import gl
import hashlib
import base64


class Login:

    def __init__(self, master):
        """Set up login GUI"""

        super().__init__()

        # set initial user type
        self.user_type = StringVar(value='admin')

        # set up db
        self.db = sqlite3.connect("database.db")
        self.c = self.db.cursor()

        # set master frame
        self.master = master
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master)

        # create welcome banner
        self.welcome_frame = tk.Frame(self.frame)
        self.welcome_frame.grid(row=0, pady=10)
        self.welcome = tk.Label(self.welcome_frame, text="It's time to check in with Djekiin Health",
                                font="TkTextFont 9 bold")
        self.welcome.pack(side="left", anchor="w")
        self.nhs_logo = tk.PhotoImage(file=r"images/login_NHS_logo.png")
        self.nhs_logo_label = tk.Label(self.welcome_frame, image=self.nhs_logo)
        self.nhs_logo_label.pack(side="right", anchor="e", padx=(5, 10))

        self.frame.pack()
        self.radio_button_frame = tk.Frame(self.frame)
        self.radio_button_frame.grid(row=1, pady=(0, 10))

        self.password_email_frame = tk.Frame(self.frame)
        self.password_email_frame.grid(row=2)
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.grid(row=3, sticky="w", padx=(12, 10), pady=(0, 5))
        row = 0
        ttk.Radiobutton(self.radio_button_frame, variable=self.user_type,
                        command=lambda: self.turn_registration(0, row), text="Admin", value="admin").grid(row=row,
                                                                                                          column=1,
                                                                                                          padx=(10, 20))
        ttk.Radiobutton(self.radio_button_frame, variable=self.user_type,
                        command=lambda: self.turn_registration(0, row), text="GP", value="GP").grid(row=row, column=2,
                                                                                                    padx=(10, 20))
        ttk.Radiobutton(self.radio_button_frame, variable=self.user_type,
                        command=lambda: self.turn_registration(1, row), text="Patient", value="Patients").grid(
            row=row, column=3,
            padx=(8, 20))

        row += 1

        # email
        self.email = tk.Entry(self.password_email_frame, width=30)
        self.email.grid(row=row, column=1, padx=20)
        row += 1

        # password
        self.password = tk.Entry(self.password_email_frame, width=30, show="*")
        self.password.grid(row=row, column=1, padx=20, pady=(2, 7))

        row = 0
        #
        self.status_label = tk.Label(self.radio_button_frame, text='I am...')
        self.status_label.grid(row=row, column=0, padx=10)
        row += 1
        # Email
        self.email_label = tk.Label(self.password_email_frame, text='Email:')
        self.email_label.grid(row=row, column=0, sticky="w", padx=0)
        row += 1
        # Password
        self.password_label = tk.Label(self.password_email_frame, text='Password:')
        self.password_label.grid(row=row, column=0, sticky="w", padx=0)
        row += 1
        # Button
        self.submit_button = tk.Button(self.button_frame, text="Submit",
                                       command=self.check_user)
        self.submit_button.grid(row=row, column=0, sticky="e")

        # register
        self.register = tk.Button(self.button_frame, text="Register as a patient")
        self.register.config(command=self.to_registration)

    def turn_registration(self, variable, row):
        """

        @param variable: 1 or 0
        @param row: current row
        @return: turns on or off the "register" button
        """
        if variable == 1:
            self.register.grid(row=row, column=1, padx=10, sticky="w")
        else:
            self.register.grid_forget()

    def to_registration(self):
        """

        @return: redirects to registration
        """
        import patient_register
        self.frame.destroy()
        patient_register.PatientRegister(self.master)

    def retrieve_userid(self, results, table):
        """

        @param results: results from the SQL query
        @param table: User Type
        @return: Returns either userID or "None" in case of an error
        """
        if results:
            for i in results:
                if table == "Patients":
                    user_id = (i[0])
                else:
                    user_id = i[7]
            try:
                if i[15] in results[0]:
                    if i[15] == "n":
                        messagebox.showerror('Oops!', "Your account hasn't been confirmed yet")
                        return "None"
            except IndexError:
                pass
            messagebox.showinfo("Success", self.email.get() + '\n You logged in successfully')

            return user_id
        else:
            messagebox.showerror('Oops!', 'Username Not Found.')
            return "None"

    def check_user(self):
        """

        @return: redirects to a relevant homepage in case of succesful login
        """
        email_value = self.email.get()
        table = self.user_type.get()
        password_values = self.password.get()
        # Password hashing
        password_hashed = base64.urlsafe_b64encode(
            hashlib.pbkdf2_hmac('sha256', password_values.encode(), b'salt', 100000)).decode("utf-8")
        if table == "admin":
            self.c.execute("SELECT * FROM Staff WHERE email=? AND password=? AND role='admin'",
                           (email_value, password_hashed))
            results = self.c.fetchall()
            user_id = self.retrieve_userid(results, table)
            if user_id != "None":
                self.master.destroy()
                newpage = tk.Tk()
                newpage.resizable(False, False)
                newpage.wm_title('Djekiin Health: Administrator')
                newpage.wm_iconbitmap('images/djekiin_logo.ico')
                newpage.config(bg='white')
                gl.main_window = newpage
                admin_home.AdminHome(newpage, user_id)

            #     Redirection to admin
        elif table == "GP":
            self.c.execute("SELECT * FROM Staff WHERE email=? AND password=? AND role='GP'",
                           (email_value, password_hashed))
            results = self.c.fetchall()
            user_id = self.retrieve_userid(results, table)
            if user_id != "None":
                self.master.destroy()
                newpage = tk.Tk()
                newpage.resizable(False, False)
                newpage.wm_title('Djekiin Health: GP')
                newpage.wm_iconbitmap('images/djekiin_logo.ico')
                newpage.config(bg="white")
                gl.main_window = newpage
                gp_home.GPHome(newpage, user_id)
        #     Redirection to GP

        if table == "Patients":
            self.c.execute("SELECT * FROM Patients WHERE email=? AND password=?",
                           (email_value, password_hashed))
            results = self.c.fetchall()
            user_id = self.retrieve_userid(results, table)
            if user_id != "None":
                self.master.destroy()
                newpage = tk.Tk()
                newpage.resizable(False, False)
                newpage.wm_title('Djekiin Health: Patient')
                newpage.wm_iconbitmap('images/djekiin_logo.ico')
                newpage.config(bg="white")
                gl.main_window = newpage
                patient_home.PatientHome(newpage, user_id)
        #     Redirection to admin


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.config(bg='white')
        Login(root)
        root.mainloop()
        pass


    main()
