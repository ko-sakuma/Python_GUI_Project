import tkinter as tk
from tkinter import ttk
import sqlite3
import navbar
import gl
import logging


class SqliteQueries:
    """A class to execute SQL queries"""

    def __init__(self, database_location):
        """
        Constructs all the necessary attributes for the SqliteQueries object.
        :param database_location: Name of the database
        """

        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    def execute(self, query, data=''):
        """
        Executes SQL query
        :param query: SQL query
        :param data: a tuple containing data for parameterized query
        :return: SQL cursor
        """

        self.c.execute(query, data)
        self.conn.commit()
        return self.c


class AdminPatientSearch(navbar.NavBarAdmin, navbar.NavBarGP):
    """A class to create GUI interface for admin patient records"""

    def __init__(self, master, user_type, user_id):
        """
        Constructs all the necessary attributes for the AdminPatientSearch object.
        :param master: TKinter master
        :param user_type: type of user - "admin" or "GP"
        """

        # Call up the menu bar items:
        self.user_type = user_type
        if self.user_type == 'admin':  # use admin nav bar
            navbar.NavBarAdmin.__init__(self, master)
        elif self.user_type == 'gp':  # use GP nav bar
            navbar.NavBarGP.__init__(self, master)

        self.master = master
        self.frame = tk.Frame(self.master)

        # Defining user_id
        self.user_id = user_id

        # Create main label frame
        self.admin_patient_frame = tk.LabelFrame(self.frame, text='Patient Records')
        self.admin_patient_frame.grid(row=0, pady=10, padx=10)

        # Create search frame
        self.search_frame = tk.LabelFrame(self.admin_patient_frame, text='Search Patients')
        self.search_frame.grid(row=0, pady=10, padx=10)
        self.search_frame.columnconfigure([0, 1], minsize=360)

        # Create entries
        self.nhs_number = tk.Entry(self.search_frame, width=40)
        self.nhs_number.grid(row=0, column=1, padx=20)

        self.f_name = tk.Entry(self.search_frame, width=40)
        self.f_name.grid(row=1, column=1, padx=20)

        self.l_name = tk.Entry(self.search_frame, width=40)
        self.l_name.grid(row=2, column=1, padx=20)

        self.gender = tk.StringVar(self.search_frame)
        self.gender_menu = tk.OptionMenu(self.search_frame, self.gender,
                                         '', 'Male', 'Female', 'Prefer not to say')
        self.gender_menu.config(width=34)
        self.gender_menu.grid(row=3, column=1, padx=20)

        self.dob = tk.Entry(self.search_frame, width=40)
        self.dob.grid(row=4, column=1, padx=20)

        self.email = tk.Entry(self.search_frame, width=40)
        self.email.grid(row=5, column=1, padx=20)

        self.phone = tk.Entry(self.search_frame, width=40)
        self.phone.grid(row=6, column=1, padx=20)

        # Create text box labels
        self.nhs_number_label = tk.Label(self.search_frame, text='NHS Number')
        self.nhs_number_label.grid(row=0, column=0)

        self.f_name_label = tk.Label(self.search_frame, text='First Name')
        self.f_name_label.grid(row=1, column=0)

        self.l_name_label = tk.Label(self.search_frame, text='Last Name')
        self.l_name_label.grid(row=2, column=0)

        self.gender_label = tk.Label(self.search_frame, text='Gender')
        self.gender_label.grid(row=3, column=0)

        self.dob_label = tk.Label(self.search_frame, text='Date of Birth (YYYY-MM-DD)')
        self.dob_label.grid(row=4, column=0)

        self.email_label = tk.Label(self.search_frame, text='Email')
        self.email_label.grid(row=5, column=0)

        self.phone_label = tk.Label(self.search_frame, text='Phone')
        self.phone_label.grid(row=6, column=0)

        # Create query button
        self.query_all_btn = tk.Button(self.search_frame, text='Show all patients',
                                       width=28, command=self.show_all_record)
        self.query_all_btn.grid(row=8, column=0, columnspan=1, pady=10, padx=10)

        self.query_btn = tk.Button(self.search_frame, text='Search patients', width=28,
                                   command=self.search_record)
        self.query_btn.grid(row=8, column=1, columnspan=1, pady=10, padx=10)

        # Create result frame
        self.result_frame = tk.LabelFrame(self.admin_patient_frame, text='Result')
        self.result_frame.grid(row=1, pady=10, padx=10)
        self.result_frame.columnconfigure([0], minsize=720)

        # create instructions
        if self.user_type == 'admin':
            instruction_text = 'Double click record to bring up details or remove the account. '
        if self.user_type == 'gp':
            instruction_text = 'Double click record to bring up details. '
        self.result_label = tk.Label(self.result_frame,
                                     text=instruction_text)
        self.result_label.grid(row=0, column=0, pady=2, padx=10, sticky='w')

        # Create treeview columns
        self.columns = ["column1", "column2", "column3", "column4", "column5",
                        "column6", "column7"]
        self.tree = ttk.Treeview(self.result_frame, column=self.columns, show="headings",
                                 selectmode="browse", height=7)
        for c in self.columns:
            self.tree.column(c, width=70)
        self.apr_scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.tree.yview)
        self.apr_scrollbar.grid(row=1, column=0, padx=(0, 10), pady=(10, 15), sticky="nes")
        self.tree.configure(yscrollcommand=self.apr_scrollbar.set)

        self.tree.heading("#1", text="NHS Number")
        self.tree.heading("#2", text="First Name")
        self.tree.heading("#3", text="Last Name")
        self.tree.heading("#4", text='Gender')
        self.tree.heading("#5", text='Date of Birth')
        self.tree.heading("#6", text='Email')
        self.tree.heading("#7", text='Phone')
        self.tree.grid(row=1, column=0, pady=10, padx=(10, 30), ipadx=100)

        # Add double click select function
        self.tree.bind('<Double-1>', self.double_click)

        self.frame.pack()

    def search_record(self):
        """
        Searches patient record
        :return: patient records matching the criteria
        """

        # Set button click indicator
        self.btn_click = "search_record"

        # Deletes current rows in tree:
        self.tree.delete(*self.tree.get_children())

        # Create class instance for the database:
        db = SqliteQueries('database.db')

        records = db.execute("SELECT NHSnumber, firstName, lastName, gender, dateOfBirth, \
                                  email, phoneNumber, userID \
                              FROM Patients\
                              WHERE NHSnumber LIKE ?\
                                  AND firstName LIKE ?\
                                  AND lastName LIKE ?\
                                  AND gender LIKE ?\
                                  AND dateOfBirth LIKE ?\
                                  AND email LIKE ?\
                                  AND replace(replace(replace(replace(replace(replace(\
                                      phoneNumber,'+',''),'-',''),' ',''),'(',''),')','')\
                                      ,'.','') LIKE ?",
                             ('%'+self.nhs_number.get()+'%',
                              '%'+self.f_name.get()+'%',
                              '%'+self.l_name.get()+'%',
                              self.gender.get()+'%',
                              '%'+self.dob.get()+'%',
                              '%'+self.email.get()+'%',
                              '%'+self.phone.get()+'%'))
        for record in records:
            self.tree.insert("", tk.END, record[7], values=record[0:7])

    def show_all_record(self):
        """
        Shows all records in the database
        :return: all records in the database
        """

        # Set button click indicator
        self.btn_click = "show_all_record"

        # Deletes current rows in tree:
        self.tree.delete(*self.tree.get_children())

        # Create class instance for the database:
        db = SqliteQueries('database.db')

        # Fetch records from SqliteQueries:
        records = db.execute("SELECT NHSnumber, firstName, lastName, gender, dateOfBirth, \
                                     email, phoneNumber, userID \
                              FROM Patients")
        for record in records:
            self.tree.insert("", tk.END, record[7], values=record[0:7])

    def double_click(self, event):
        """
        Makes two buttons appear once the user double clicks on a patient
        :param event: double click event
        :return: "show details" and "Delete record button"
        """

        row_id = self.tree.identify_row(event.y)
        print("Patient ID:", row_id)

        try:
            self.show_details.grid_forget()
        except Exception:
            pass
        try:
            self.delete.grid_forget()
        except Exception:
            pass

        if self.user_type == "admin":
            self.show_details = tk.Button(self.result_frame, width=28, text="Show details",
                                          command=lambda: self.show_patient_details(row_id))
            self.delete = tk.Button(self.result_frame, width=28, text="Delete record",
                                    command=lambda: self.delete_patient(row_id))
            self.show_details.grid(row=2, column=0, pady=10, padx=(70, 10), sticky='w')
            self.delete.grid(row=2, column=0, pady=10, padx=(10, 70), sticky='e')
        elif self.user_type == 'gp':
            self.show_details = tk.Button(self.result_frame, width=28, text="Show details",
                                          command=lambda: self.show_patient_details(row_id))
            self.show_details.grid(row=2, column=0, pady=10, padx=(10, 10))

    def show_patient_details(self, row_id):
        """
        Brings up patient details by clicking the 'show details' button.
        :param row_id: patient ID
        :return: patient details in a new window (patient_my_record.py)
        """

        # Create class instance for the database:
        db = SqliteQueries('database.db')

        # Fetch email of a Staff
        staff_email_record = db.execute(f"SELECT email FROM Staff WHERE userID={self.user_id}")

        for email in staff_email_record:
            staff_email = email[0]

        # Fetch email of a Patient
        patient_email_record = db.execute(f"SELECT email FROM Patients WHERE userID={row_id}")

        for email in patient_email_record:
            patient_email = email[0]

        # Insert the following information into log
        logger.info(" Staff {0} ({1}) viewed Patient {2}'s ({3}) profile".format(self.user_id,
                                                                                 staff_email,
                                                                                 row_id,
                                                                                 patient_email))

        # Delete buttons
        self.show_details.grid_forget()
        if self.user_type == "admin":
            self.delete.grid_forget()

        # Call up patient page
        import patient_my_record

        sub_window = tk.Tk()
        sub_window.wm_title('Djekiin Health: Patient Records')
        sub_window.wm_iconbitmap('images/djekiin_logo.ico')
        patient_my_record.PatientRecord(sub_window, row_id, "admin")
        sub_window.mainloop()

    def delete_patient(self, row_id):
        """
        Deletes a record
        :param row_id: patient id
        :return: delete a record
        """

        # delete buttons
        self.show_details.grid_forget()
        self.delete.grid_forget()

        # If the user confirmed the deletion
        def delete_yes():
            self.delete_warning.destroy()
            db = SqliteQueries('database.db')
            db.execute("DELETE FROM Patients WHERE userID = ?",
                       (row_id,))

            # Refresh results
            if self.btn_click == "show_all_record":
                self.show_all_record()
            elif self.btn_click == "search_record":
                self.search_record()
            else:
                pass

        # If the user did not confirm the deletion
        def delete_no():
            self.delete_warning.destroy()
            pass

        # Pop up box for confirmation
        self.delete_warning = tk.Tk()
        delete_label = tk.Label(self.delete_warning, text='You are about to delete the record. Continue? ')
        delete_label.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
        delete_yes = tk.Button(self.delete_warning, text='Yes', width=15, command=delete_yes)
        delete_yes.grid(row=2, column=0, columnspan=1, pady=10, padx=10)
        delete_no = tk.Button(self.delete_warning, text='No', width=15, command=delete_no)
        delete_no.grid(row=2, column=1, columnspan=1, pady=10, padx=10)
        self.delete_warning.mainloop()


# Create Log that records which Staff viewed whose Patient Record at what time.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(message)s')

file_handler = logging.FileHandler('ViewersLog.txt')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health: Administrator')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        gl.main_window = root
        AdminPatientSearch(root, "admin", 2)
        root.mainloop()


    main()
