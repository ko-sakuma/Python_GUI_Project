import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import navbar
import sqlite3


class SqliteQueries:
    def __init__(self, database_location):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    def execute(self, query, data):
        self.c.execute(query, data)
        self.conn.commit()
        return self.c

    def fetch_patient_info_from_column(self, patient_id, column):
        self.c.execute(f"SELECT {column} FROM Patients WHERE userID = {patient_id}")
        records = self.c.fetchone()
        var = records[0]
        return var


class PatientProfile(navbar.NavBarPatient):
    def __init__(self, master, patient_id):
        # Call up the menu bar items:
        super().__init__(master)

        self.patient_id = patient_id
        self.db = SqliteQueries("database.db")
        self.master = master
        self.frame = tk.Frame(self.master)

        self.labelframe = tk.LabelFrame(self.frame, text="My Profile")
        self.labelframe.grid(column=0, row=7, padx=20, pady=60)

        # Create frames for the input fields

        # First Name
        entry_text_first_name = tk.StringVar()
        self.f_name = tk.Entry(self.labelframe, textvariable=entry_text_first_name, width=30)
        entry_text_first_name.set(self.db.fetch_patient_info_from_column(self.patient_id, "firstName"))
        self.f_name.grid(row=0, column=1, padx=20)
        self.f_name_label = tk.Label(self.labelframe, text='First Name')
        self.f_name_label.grid(row=0, column=0)

        # Last Name
        entry_text_last_name = tk.StringVar()
        self.l_name = tk.Entry(self.labelframe, textvariable=entry_text_last_name, width=30)
        entry_text_last_name.set(self.db.fetch_patient_info_from_column(self.patient_id, "lastName"))
        self.l_name.grid(row=1, column=1, padx=20)
        self.l_name_label = tk.Label(self.labelframe, text='Last Name')
        self.l_name_label.grid(row=1, column=0)

        # Gender
        self.n = tk.StringVar()
        self.gender = ttk.Combobox(self.labelframe, width=29, textvariable=self.n, state='readonly')
        self.gender['values'] = ('Please choose',
                                 'Female',
                                 'Male',
                                 'Other',
                                 'Prefer not to say')
        if self.db.fetch_patient_info_from_column(self.patient_id, "gender") == 'Male':
            self.gender.current(2)
        elif self.db.fetch_patient_info_from_column(self.patient_id, "gender") == 'Female':
            self.gender.current(1)
        elif self.db.fetch_patient_info_from_column(self.patient_id, "gender") == 'Other':
            self.gender.current(3)
        else:
            self.gender.current(4)
        self.gender.grid(column=1, row=2, padx=20)
        self.gender_label = tk.Label(self.labelframe, text='Gender')
        self.gender_label.grid(row=2, column=0)

        # Date of Birth
        entry_text_date_of_birth = tk.StringVar()
        self.dob = tk.Entry(self.labelframe, textvariable=entry_text_date_of_birth, width=30)
        entry_text_date_of_birth.set(self.db.fetch_patient_info_from_column(self.patient_id, "dateOfBirth"))
        self.dob.grid(row=3, column=1, padx=20)
        self.dob_label = tk.Label(self.labelframe, text='Date of Birth')
        self.dob_label.grid(row=3, column=0)

        # Full Address
        entry_text_address = tk.StringVar()
        self.address = tk.Entry(self.labelframe, textvariable=entry_text_address, width=30)
        entry_text_address.set(self.db.fetch_patient_info_from_column(self.patient_id, "address"))
        self.address.grid(row=4, column=1, padx=20)
        self.address_label = tk.Label(self.labelframe, text='Full Address')
        self.address_label.grid(row=4, column=0)

        # Email Address
        entry_text_email = tk.StringVar()
        self.email = tk.Entry(self.labelframe, textvariable=entry_text_email, width=30)
        entry_text_email.set(self.db.fetch_patient_info_from_column(self.patient_id, "email"))
        self.email.grid(row=5, column=1, padx=20)
        self.email_label = tk.Label(self.labelframe, text='Email')
        self.email_label.grid(row=5, column=0)

        # Phone Number
        entry_text_phone_number = tk.StringVar()
        self.phone = tk.Entry(self.labelframe, textvariable=entry_text_phone_number, width=30)
        entry_text_phone_number.set(self.db.fetch_patient_info_from_column(self.patient_id, "phoneNumber"))
        self.phone.grid(row=6, column=1, padx=20)
        self.phone_label = tk.Label(self.labelframe, text='Phone')
        self.phone_label.grid(row=6, column=0)

        # NHS Number
        entry_text_nhs_number = tk.StringVar()
        self.nhs_num = tk.Entry(self.labelframe, textvariable=entry_text_nhs_number, width=30)
        entry_text_nhs_number.set(self.db.fetch_patient_info_from_column(self.patient_id, "NHSnumber"))
        self.nhs_num.grid(row=7, column=1, padx=20)
        self.nhs_num_label = tk.Label(self.labelframe, text='NHS Number')
        self.nhs_num_label.grid(row=7, column=0)

        # Create a submit button
        self.submit_btn = tk.Button(self.labelframe, text='Save Changes', command=self.submit)
        self.submit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        self.frame.pack()

    def submit(self):
        con = sqlite3.connect("database.db")
        c = con.cursor()
        query = '''UPDATE Patients SET gender = ?, dateOfBirth = ?, NHSnumber = ?, address = ?, firstName= ?, 
        lastName= ?, phoneNumber= ?, email= ? WHERE userID = ? '''
        values = (
            self.gender.get(), self.dob.get(), self.nhs_num.get(), self.address.get(), self.f_name.get(),
            self.l_name.get(), self.phone.get(), self.email.get(), self.patient_id)
        c.execute(query, values)
        con.commit()
        messagebox.showinfo("Success", 'Changes made successfully')
        con.close()


if __name__ == '__main__':
    def main():
        import gl
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health: Patient')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        gl.main_window = root
        PatientProfile(root, 2)

        root.mainloop()


    main()

# #sqlite class:
