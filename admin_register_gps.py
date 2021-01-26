import navbar
import tkinter as tk
from tkinter import messagebox
import sqlite3
import gl
import hashlib
import base64


class SqliteQueries:
    def __init__(self, database_location):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    def execute(self, query, data=''):
        self.c.execute(query, data)
        self.conn.commit()
        return self.c


class AdminRegisterGP(navbar.NavBarAdmin):
    def __init__(self, master):

        # Call up the menu bar items:
        super().__init__(master)

        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Create the square grid
        self.labelframe = tk.LabelFrame(self.frame, text="Register GPs")
        self.labelframe.grid(column=0, row=13, padx=40, pady=60)

        row = 0
        # First Name
        self.firstName = tk.Entry(self.labelframe, width=30)
        self.firstName.grid(row=row, column=1, padx=20)
        self.firstName_label = tk.Label(self.labelframe, text='First Name')
        self.firstName_label.grid(row=row, column=0)
        row += 1

        # Last Name
        self.lastName = tk.Entry(self.labelframe, width=30)
        self.lastName.grid(row=row, column=1, padx=20)
        self.lastName_label = tk.Label(self.labelframe, text='Last Name')
        self.lastName_label.grid(row=row, column=0)
        row += 1

        # Full Address
        self.address = tk.Entry(self.labelframe, width=30)
        self.address.grid(row=row, column=1, padx=20)
        self.address_label = tk.Label(self.labelframe, text='Full Address')
        self.address_label.grid(row=row, column=0)
        row += 1

        # Email
        self.email = tk.Entry(self.labelframe, width=30)
        self.email.grid(row=row, column=1, padx=20)
        self.email_label = tk.Label(self.labelframe, text='Email')
        self.email_label.grid(row=row, column=0)
        row += 1

        # Phone Number
        self.phoneNumber = tk.Entry(self.labelframe, width=30)
        self.phoneNumber.grid(row=row, column=1, padx=20)
        self.phoneNumber_label = tk.Label(self.labelframe, text='Phone')
        self.phoneNumber_label.grid(row=row, column=0)
        row += 1

        # Password
        self.password = tk.Entry(self.labelframe, width=30)
        self.password.grid(row=row, column=1, padx=20)
        self.password_label = tk.Label(self.labelframe, text='Password')
        self.password_label.grid(row=row, column=0)
        row += 1

        # Create submit button to register
        self.submit_btn = tk.Button(self.labelframe, text='Register GP', command=self.submit)
        self.submit_btn.grid(row=row, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        row += 1

    def submit(self):
        if self.firstName.get() == "":
            return messagebox.showinfo("Success", 'First Name is missing')

        elif self.lastName.get() == "":
            return messagebox.showinfo("Success", 'Last Name is missing')

        elif self.address.get() == "":
            return messagebox.showinfo("Success", 'Full Address is missing')

        elif self.email.get() == "":
            return messagebox.showinfo("Success", 'Email is missing')

        elif self.phoneNumber.get() == "":
            return messagebox.showinfo("Success", 'Phone Number is missing')

        elif self.password.get() == "":
            return messagebox.showinfo("Success", 'Password is missing')

        else:
            # Call up SqliteQueries class
            db = SqliteQueries('database.db')

            # Password hashing
            password_hashed = base64.urlsafe_b64encode(
                hashlib.pbkdf2_hmac('sha256', self.password.get().encode(), b'salt', 100000)).decode("utf-8")

            # Use the insert user method from the SqliteQueries class:
            db.execute(
                "INSERT INTO Staff (firstName, lastName, email, phoneNumber, password, role, address) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.firstName.get(), self.lastName.get(), self.email.get(), self.phoneNumber.get(),
                 password_hashed, 'GP', self.address.get()))

            # Show a pop up upon a successful registration
            messagebox.showinfo("Success", 'GP is successfully registered')

            # Delete the user inputs in the fields upon submission
            self.firstName.delete(0, tk.END)
            self.lastName.delete(0, tk.END)
            self.address.delete(0, tk.END)
            self.email.delete(0, tk.END)
            self.phoneNumber.delete(0, tk.END)
            self.password.delete(0, tk.END)


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        gl.main_window = root
        root.wm_title('Djekiin Health: Administrator')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.resizable(False, False)
        AdminRegisterGP(root)
        root.mainloop()


    main()
