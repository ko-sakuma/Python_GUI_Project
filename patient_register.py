import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import hashlib
import base64


class SQLQueries:
    def __init__(self, database_path):
        self.db = sqlite3.connect(database_path)
        self.c = self.db.cursor()

    def add_user(self, dict):
        """

        @param dict: dictionary with submitted values
        @return: returns succesful record insert. Returns "None" in case of an error
        """
        emptyfields = False
        for key, value in dict.items():
            if (len(value) == 0) or (value == "Please choose"):
                emptyfields = True
                break

        if not emptyfields:
            statement = "INSERT INTO Patients ("
            for key, value in dict.items():
                statement = statement + key + ","

            statement = statement[:-1] + ") VALUES ('"
            for key, value in dict.items():
                statement = statement + str(value) + "','"
            statement = statement[:-1] + ")"
            print(statement[:-2] + ")")
            self.c.execute(statement[:-2] + ")")
            self.db.commit()
            print(self.c.lastrowid)
            messagebox.showinfo(title="Successfully registered", message="Give us some time to confirm your account")
            return
        else:
            messagebox.showinfo(title="Some fields are empty", message="Please complete all fields")
            return "None"


class PatientRegister:

    def __init__(self, master):
        """Initiating the page, displaying input fields"""

        # call up the menu bar items:
        self.db = SQLQueries("database.db")
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.master.resizable(False, False)
        row = 0
        self.parametersList = {}

        # First Name
        self.firstName = tk.Entry(self.frame, width=30)
        self.firstName.grid(row=row, column=1, padx=20)
        self.parametersList["firstName"] = self.firstName
        row += 1
        # Last name
        self.lastName = tk.Entry(self.frame, width=30)
        self.lastName.grid(row=row, column=1, padx=20)
        self.parametersList["lastName"] = self.lastName
        row += 1
        # Email
        self.email = tk.Entry(self.frame, width=30)
        self.email.grid(row=row, column=1, padx=20)
        self.parametersList["email"] = self.email
        row += 1
        # password
        self.password = tk.Entry(self.frame, width=30, show="*")
        self.password.grid(row=row, column=1, padx=20)
        self.parametersList["password"] = self.password
        row += 1
        # gender
        self.gender = StringVar()
        gender_values = ("Please choose", "Female", "Male", "Other", "Prefer not to say")
        self.gender_sel = ttk.Combobox(self.frame, values=gender_values, textvariable=self.gender, state="readonly")
        self.gender_sel.current(0)
        self.gender_sel.grid(row=row, column=1, padx=20)
        self.parametersList["gender"] = self.gender_sel
        row += 1

        #    Date of Birth

        self.date_of_birth = tk.Entry(self.frame, width=30)
        self.date_of_birth.grid(row=row, column=1, padx=20)
        self.parametersList["dateOfBirth"] = self.date_of_birth
        row += 1
        # NHS number
        self.nhs_number = tk.Entry(self.frame, width=30)
        self.nhs_number.grid(row=row, column=1, padx=20)
        self.parametersList["NHSnumber"] = self.nhs_number
        row += 1
        # Address (Maybe change to to different input field)
        self.address = tk.Entry(self.frame, width=30)
        self.address.grid(row=row, column=1, padx=20)
        self.parametersList["address"] = self.address
        row += 1
        # Phone_number
        self.phone_number = tk.Entry(self.frame, width=30)
        self.phone_number.grid(row=row, column=1, padx=20)
        self.parametersList["phoneNumber"] = self.phone_number
        row += 1
        # Height
        self.height = Spinbox(self.frame, from_=100, to=300)
        self.height.grid(row=row, column=1, padx=20)
        self.parametersList["height"] = self.height
        row += 1
        # Weight
        self.weight = Spinbox(self.frame, from_=0, to=300)
        self.weight.grid(row=row, column=1, padx=20)
        self.parametersList["weight"] = self.weight
        row += 1
        # Smoking behavior
        self.smoking = StringVar()
        smoking_values = ("Please choose",
                          "Never smoked", "Smoked before but stopped", "Smoke ocassionaly", "Smoke frequently")
        self.smoking_sel = ttk.Combobox(self.frame, values=smoking_values, textvariable=self.smoking, state="readonly")
        self.smoking_sel.current(0)
        self.smoking_sel.grid(row=row, column=1, padx=20)
        self.parametersList["smokingBehavior"] = self.smoking_sel
        row += 1
        # Drinking behavior
        self.drinking = StringVar()
        drinking_values = (
            "Please choose", "Every day", "5 to 6 times a week", "3 to 4 times a week", "Twice a week", "Once a week",
            "2 to 3 times a month", "Once a month", "3 to 11 times in the past year", "1 or 2 times in the past year")
        self.drinking_sel = ttk.Combobox(self.frame, values=drinking_values, textvariable=self.drinking,
                                         state="readonly")
        self.drinking_sel.current(0)
        self.drinking_sel.grid(row=row, column=1, padx=20)
        self.parametersList["drinkingBehavior"] = self.drinking_sel
        # confirmed
        self.confirmed = StringVar(self.frame, value='n')
        # confirmed = Entry(self.frame, textvariable=v)
        self.parametersList["confirmed"] = self.confirmed
        row += 1
        # Exercise scale
        self.w1 = Scale(self.frame, orient=HORIZONTAL, from_=0, to=10)
        self.w1.grid(row=row, column=1, padx=20)
        self.parametersList["exercise"] = self.w1

        row = 0
        # First Name

        self.f_name_label = tk.Label(self.frame, text='First Name')
        self.f_name_label.grid(row=row, column=0)
        row += 1

        # Last Name
        self.l_name_label = tk.Label(self.frame, text='Last Name')
        self.l_name_label.grid(row=row, column=0)
        row += 1
        # Email
        self.email_label = tk.Label(self.frame, text='Email')
        self.email_label.grid(row=row, column=0)
        row += 1
        # Password
        self.password_label = tk.Label(self.frame, text='Password')
        self.password_label.grid(row=row, column=0)
        row += 1

        # Gender
        self.gender_label = tk.Label(self.frame, text='Gender')
        self.gender_label.grid(row=row, column=0)
        row += 1
        # Date of Birth
        self.date_of_birth_label = tk.Label(self.frame, text='Date of Birth (YYYY-MM-DD)')
        self.date_of_birth_label.grid(row=row, column=0)
        row += 1
        # NHSnumber
        self.nhs_label = tk.Label(self.frame, text='NHSnumber')
        self.nhs_label.grid(row=row, column=0)
        row += 1
        # Address
        self.adress_label = tk.Label(self.frame, text='Address')
        self.adress_label.grid(row=row, column=0)
        row += 1
        # Phone_number
        self.adress_label = tk.Label(self.frame, text='Phone Number')
        self.adress_label.grid(row=row, column=0)
        row += 1
        # Height
        self.height_label = tk.Label(self.frame, text='Height (cm)')
        self.height_label.grid(row=row, column=0)
        row += 1
        # Weight
        self.weight_label = tk.Label(self.frame, text='Weight (kg)')
        self.weight_label.grid(row=row, column=0)
        row += 1
        # Smoking habits
        self.smoking_label = tk.Label(self.frame, text='Smoking habits')
        self.smoking_label.grid(row=row, column=0)
        row += 1
        # Drinking habits
        self.drinking_label = tk.Label(self.frame, text='Drinking habits')
        self.drinking_label.grid(row=row, column=0)
        row += 1
        # Exercise habits
        self.exercise_label = tk.Label(self.frame,
                                       text='How physically active are you? \n'
                                            'Think of any physical activity\n (job, gardening, '
                                            'walking commute, gym exercise.)')
        self.exercise_label.grid(row=row, column=0)
        row += 1

        # Button
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.submit)
        self.submit_button.grid(row=row, column=1)
        row += 1
        # Back to login

        self.to_login_button = tk.Button(self.frame, text="Already registered? Log in", command=self.to_login)
        self.to_login_button.grid(row=row, column=1)

    def to_login(self):
        """

        @return: Redirects to login
        """
        import login
        self.frame.destroy()
        login.Login(self.master)

    def submit(self):
        """

        @return: processes submitted values
        """

        self.submittedValues = dict(self.parametersList)
        for key, value in self.parametersList.items():
            # print(i)
            if value != "n":
                parameter = value.get()
            else:
                parameter = "n"
            print(key + ":" + str(parameter))
            self.submittedValues[key] = str(value.get())
        print('before hashing', self.submittedValues)
        self.submittedValues['password'] = base64.urlsafe_b64encode(
            hashlib.pbkdf2_hmac('sha256', self.submittedValues['password'].encode(), b'salt', 100000)).decode("utf-8")
        print('after hashing', self.submittedValues)
        result = self.db.add_user(self.submittedValues)
        if result != "None":
            self.to_login()


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health: Patient Register')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        PatientRegister(root)
        root.mainloop()


    main()
