import navbar
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
import hashlib
import os
import base64
from tkinter import messagebox

class SqliteQueries:
    def __init__(self, database_path):
        self.path = database_path

    def add_user(self, dict):
        '''
        Adding patient details into the Patient table on the database
        @param dict:
        @return:
        '''
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()
        statement = "INSERT INTO Patients ("
        for key, value in dict.items():
            statement = statement + key + ","

        statement = statement[:-1] + ") VALUES ("
        for key, value in dict.items():
            statement = statement + "\'{0}\'".format(value) + ","
        statement = statement[:-1] + ")"
        self.c.execute("{0}".format(statement))
        self.conn.commit()
        self.conn.close()

    def select_users(self):
        ''' getting patient details from the database'''
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()

        self.c.execute(
            "SELECT firstName, lastName, gender, dateOfBirth, NHSnumber,email, confirmed "
            "FROM Patients "
            "WHERE confirmed = 'n'"
        )
        users = self.c.fetchall()
        return users
        self.conn.close()

    def confirm_patient(self, ID):
        '''
        Changing the status of the patient to confirmed
        @param ID: NHS number of the patient in question
        @return:
        '''
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()
        self.ID = ID
        try:
            self.c.execute(f"UPDATE Patients SET confirmed = 'y' WHERE NHSnumber = {self.ID} ")
            self.conn.commit()
        except:
            messagebox.showerror("The user has incorrect values in its form", "The user has incorrect values in its form, please remove user from the database")

        self.conn.close()

    def delete_patient(self, ID):
        ''' Deletes the patient details from the daexcept:
            messagebox.showerror("The user has incorrect values in its form", "The user has incorrect values in its form, please remove user from the database")
tabase'''
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()
        self.ID = ID

        try:
            self.c.execute(f" DELETE from Patients WHERE NHSnumber = {self.ID} ")
            self.conn.commit()
        except:
            messagebox.showerror("The user has incorrect values in its form", "The user has incorrect values in its form, please remove user from the database")

        self.conn.close()


class admin_confirmation_patients(navbar.NavBarAdmin):

    def __init__(self, master):
        '''
        Initialising the page
        @param master: This is the Tkinter frame, i.e. the GUI
        '''
        super().__init__(master)

        self.master = master
        self.db = SqliteQueries("database.db")
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.frame3 = tk.LabelFrame(self.frame, text="Confirm Patients")
        self.text = tk.Label(self.frame3, text=" Double click a patient in order to confirm or remove an account")
        self.text.pack()

        self.columns = ['First Name', 'Last Name', 'Sex', 'Date of B', 'NHS Number', 'Email', 'S']
        self.tree = ttk.Treeview(self.frame3, column=self.columns, show="headings", height=10)

        for c in self.columns:
            self.tree.column(c, width=60 + 5 * len(c))

        self.tree.heading("#1", text="First Name")
        self.tree.heading("#2", text="Last Name")
        self.tree.heading("#3", text="Gender")
        self.tree.heading("#4", text='Date of birth')
        self.tree.heading("#5", text="NHS Number")
        self.tree.heading("#6", text='Email')
        self.tree.heading("#7", text='Status')
        self.tree.bind('<Double-1>', self.double_click)
        self.tree.pack(padx=10, pady=10)
        self.get_users()

        self.frame2 = tk.LabelFrame(self.frame, text="Register Patients")
        self.frame2.pack()
        self.frame3.pack(padx=10, pady=10)

        row = 0
        self.parametersList = {}

        # First Name
        self.firstName = tk.Entry(self.frame2, width=30)
        self.firstName.grid(row=row, column=1, padx=20)
        self.parametersList["firstName"] = self.firstName
        row += 1

        # Last name
        self.lastName = tk.Entry(self.frame2, width=30)
        self.lastName.grid(row=row, column=1, padx=20)
        self.parametersList["lastName"] = self.lastName
        row += 1

        # Email
        self.email = tk.Entry(self.frame2, width=30)
        self.email.grid(row=row, column=1, padx=20)
        self.parametersList["email"] = self.email
        row += 1

        # Password
        self.password = tk.Entry(self.frame2, width=30, show="*")
        self.password.grid(row=row, column=1, padx=20)
        self.parametersList["password"] = self.password
        row += 1

        # Gender
        self.gender = StringVar()
        gender_values = ("Please choose", "Female", "Male", "Other", "Prefer not to say")
        self.gender_sel = ttk.Combobox(self.frame2, values=gender_values, textvariable=self.gender, state="readonly")
        self.gender_sel.current(0)
        self.gender_sel.grid(row=row, column=1, padx=20)
        self.parametersList["gender"] = self.gender_sel
        row += 1

        # Date of Birth
        self.date_of_birth = tk.Entry(self.frame2, width=30)
        self.date_of_birth.grid(row=row, column=1, padx=20)
        self.parametersList["dateOfBirth"] = self.date_of_birth
        row += 1

        # NHS number
        self.nhs_number = tk.Entry(self.frame2, width=30)
        self.nhs_number.grid(row=row, column=1, padx=20)
        self.parametersList["NHSnumber"] = self.nhs_number
        row += 1

        # Address
        self.address = tk.Entry(self.frame2, width=30)
        self.address.grid(row=row, column=1, padx=20)
        self.parametersList["address"] = self.address
        row += 1

        # Phone_number
        self.phone_number = tk.Entry(self.frame2, width=30)
        self.phone_number.grid(row=row, column=1, padx=20)
        self.parametersList["phoneNumber"] = self.phone_number
        row += 1

        # Height
        self.height = Spinbox(self.frame2, from_=100, to=300)
        self.height.grid(row=row, column=1, padx=20)
        self.parametersList["height"] = self.height
        row += 1

        # Weight
        self.weight = Spinbox(self.frame2, from_=0, to=300)
        self.weight.grid(row=row, column=1, padx=20)
        self.parametersList["weight"] = self.weight
        row += 1

        # Smoking behavior
        self.smoking = StringVar()
        smoking_values = ("Please choose", "Never smoked", "Smoked before but stopped",
                          "Smoke occasionally", "Smoke frequently")
        self.smoking_sel = ttk.Combobox(self.frame2, values=smoking_values, textvariable=self.smoking, state="readonly")
        self.smoking_sel.current(0)
        self.smoking_sel.grid(row=row, column=1, padx=20)
        self.parametersList["smokingBehavior"] = self.smoking_sel
        row += 1

        # Drinking behavior
        self.drinking = StringVar()
        drinking_values = ("Please choose", "Every day", "5 to 6 times a week", "3 to 4 times a week",
                           "Twice a week", "Once a week", "2 to 3 times a month", "Once a month",
                           "3 to 11 times in the past year", "1 or 2 times in the past year")
        self.drinking_sel = ttk.Combobox(self.frame2, values=drinking_values,
                                         textvariable=self.drinking, state="readonly")
        self.drinking_sel.current(0)
        self.drinking_sel.grid(row=row, column=1, padx=20)
        self.parametersList["drinkingBehavior"] = self.drinking_sel
        row += 1

        # Exercise scale
        self.w1 = Scale(self.frame2, orient=HORIZONTAL, from_=0, to=10)
        self.w1.grid(row=row, column=1, padx=20)
        self.parametersList["exercise"] = self.w1

        row = 0
        # First Name
        self.f_name_label = tk.Label(self.frame2, text='First Name')
        self.f_name_label.grid(row=row, column=0)
        row += 1

        # Last Name
        self.l_name_label = tk.Label(self.frame2, text='Last Name')
        self.l_name_label.grid(row=row, column=0)
        row += 1

        # Email
        self.email_label = tk.Label(self.frame2, text='Email')
        self.email_label.grid(row=row, column=0)
        row += 1

        # Password
        self.password_label = tk.Label(self.frame2, text='Password')
        self.password_label.grid(row=row, column=0)
        row += 1

        # Gender
        self.gender_label = tk.Label(self.frame2, text='Gender')
        self.gender_label.grid(row=row, column=0)
        row += 1

        # Date of Birth
        self.date_of_birth_label = tk.Label(self.frame2, text='Date of Birth (YYYY-MM-DD)')
        self.date_of_birth_label.grid(row=row, column=0)
        row += 1

        # NHSnumber
        self.nhs_label = tk.Label(self.frame2, text='NHSnumber')
        self.nhs_label.grid(row=row, column=0)
        row += 1

        # Address
        self.adress_label = tk.Label(self.frame2, text='Address')
        self.adress_label.grid(row=row, column=0)
        row += 1

        # Phone_number
        self.adress_label = tk.Label(self.frame2, text='Phone Number')
        self.adress_label.grid(row=row, column=0)
        row += 1

        # Height
        self.height_label = tk.Label(self.frame2, text='Height (cm)')
        self.height_label.grid(row=row, column=0)
        row += 1

        # Weight
        self.weight_label = tk.Label(self.frame2, text='Weight (kg)')
        self.weight_label.grid(row=row, column=0)
        row += 1

        # Smoking habits
        self.smoking_label = tk.Label(self.frame2, text='Smoking habits')
        self.smoking_label.grid(row=row, column=0)
        row += 1

        # Drinking habits
        self.drinking_label = tk.Label(self.frame2, text='Drinking habits')
        self.drinking_label.grid(row=row, column=0)
        row += 1

        self.exercise_label = tk.Label(self.frame2,
                                       text='How physically active are you? \nThink of any physical activity\n '
                                            '(job, gardening, walking commute, gym exercise.)')
        self.exercise_label.grid(row=row, column=0)
        row += 1

        # Button
        self.submit_button = tk.Button(self.frame2, text="Submit", command=self.submit)
        self.submit_button.grid(row=row, column=1)


    def submit(self):
        """
        Submits the details of the user into the database
        @return: none
        """

        #checking if all fields are completed:
        for key in self.parametersList:
            if not self.parametersList[key].get():
                messagebox.showerror("Missing fields", "Please enter all the fields to complete registration, and press submit"
                                             " once more.")
                return
        submittedValues = dict(self.parametersList)
        try:
            check=type(int(self.parametersList["NHSnumber"].get()))
            for key, value in self.parametersList.items():
                parameter = value.get()
                submittedValues[key] = str(value.get())
            print('before hashing', submittedValues)
            submittedValues['password'] = base64.urlsafe_b64encode(
                hashlib.pbkdf2_hmac('sha256', submittedValues['password'].encode(), b'salt', 100000)).decode("utf-8")
            print('after hashing', submittedValues)
            self.db.add_user(submittedValues)
            self.remove_treeview_values()
            self.get_users()
            tk.messagebox.showinfo("Success",
                                "Registration Form submitted succesfully")
        except:
            messagebox.showerror("NHSnumber erros",'You have inputted the incorrect NHS number')



    def get_users(self):
        '''
        Inserts the details of the users who have not yet been confirmed into the treeview
        @return: none
        '''
        records = self.db.select_users()
        for record in records:
            self.tree.insert("", 'end', values=record)

    def remove_treeview_values(self):
        '''
        removes patient details from treeview
        @return:
        '''
        for patient in self.tree.get_children():
            self.tree.delete(patient)

    def double_click(self, action):
        '''
        This function makes two buttons appear once the user double clicks on a patient
        @param action:
        @return:
        '''
        item = self.tree.selection()
        NHS_N = self.tree.item(item, "values")[4]
        try:
            self.confirm.forget()
            self.delete.forget()
            self.confirm = tk.Button(self.frame3, text="Confirm", command=lambda: self.confirm_patient(NHS_N))
            self.delete = tk.Button(self.frame3, text="Delete", command=lambda: self.delete_patient(NHS_N))
            self.confirm.pack(side="left", padx=100)
            self.delete.pack(side="right", padx=100)
        except:
            self.confirm = tk.Button(self.frame3, text="Confirm", command=lambda: self.confirm_patient(NHS_N))
            self.delete = tk.Button(self.frame3, text="Delete", command=lambda: self.delete_patient(NHS_N))
            self.confirm.pack(side="left", padx=100)
            self.delete.pack(side="right", padx=100)


    def confirm_patient(self, NHS_N):
        '''
        Patients who have registered get confirmed
        @param NHS_N: patient's NHS number
        @return:
        '''
        self.db.confirm_patient(NHS_N)
        self.remove_treeview_values()
        self.get_users()
        self.confirm.forget()
        self.delete.forget()

    def delete_patient(self, NHS_N):
        '''
        Removes the details of the patient if the admin decides to delete them
        @param NHS_N: patient's NHS number
        @return:
        '''
        self.db.delete_patient(NHS_N)
        self.remove_treeview_values()
        self.get_users()
        self.confirm.forget()
        self.delete.forget()


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health: Administrator')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.config(bg="white")
        admin_confirmation_patients(root)
        root.mainloop()


    main()
