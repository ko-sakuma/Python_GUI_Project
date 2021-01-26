import tkinter as tk
from tkinter import ttk
import sqlite3
import navbar


# the sqlite queries:
class SqliteQueries:
    def __init__(self, database_location):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    def execute(self, query, data):
        self.c.execute(query, data)
        self.conn.commit()
        return self.c

    def fetch_all_query(self, query):
        self.c.execute(query)
        return self.c.fetchall()

    def fetch_all_rows_from_a_table(self, table_entered):
        self.c.execute(f"SELECT * FROM {table_entered}")
        records = self.c.fetchall()
        return records

    def fetch_patient_full_name(self, patient_id):
        self.c.execute(f"SELECT firstName, lastName FROM Patients WHERE userID = {patient_id}")
        records = self.c.fetchall()
        name = ""
        for row in records:
            name = str(row[0]) + " " + str(row[1])
        return name

    def update(self, table_entered, columns, data, conditionals):
        """
        :param table_entered: table (and column names if required) in db
        :param columns: attributes to update in db
        :param data: data to update record with
        :param conditionals: set which records you want to update
        :return: inserts new values into record
        """

        # Prepares column update expression with placeholder ? for SET part of query
        columns_to_update = ""
        for x in columns:
            columns_to_update += ', ' + ('%s = ?' % x)
        columns_to_update = columns_to_update[2:]

        # Returns update query query
        return self.execute("UPDATE %s SET %s WHERE %s" % (table_entered, columns_to_update, conditionals), data)

    def fetch_patient_age(self, patient_id):
        self.c.execute(f"""SELECT date('now') - dateOfBirth
                        FROM Patients WHERE userID = {patient_id}""")
        records = self.c.fetchone()
        age = str(records[0])
        return age

    def fetch_patient_info_from_column(self, patient_id, column):
        self.c.execute(f"SELECT {column} FROM Patients WHERE userID = {patient_id}")
        records = self.c.fetchone()
        var = records[0]
        return var

    def calculate_bmi(self, patient_id):
        self.c.execute(f"SELECT weight, height FROM Patients WHERE userID={patient_id}")
        records = self.c.fetchone()
        weight = records[0]
        height = records[1]
        bmi = weight / ((height / 100) ** 2)
        return round(bmi, 1)

    def retrieve_gp_appointments(self, patient_id):
        self.c.execute(f"""SELECT date(A.datetime), "Dr. " || S.firstName || " " || S.lastName as fullName
                        FROM Staff S 
                        INNER JOIN Appointments A on S.userID = A.doctorID
                        WHERE A.patientID = {patient_id}
                        AND A.dateTime <= date('now')""")
        records = self.c.fetchall()
        return records


class PatientRecord(navbar.NavBarPatient):
    def __init__(self, master, person_id, user_type):

        self.user_type = user_type
        self.person_id = person_id
        self.db = SqliteQueries("database.db")

        # creating notebook and tabs:
        self.master = master

        # call up the menu bar items:
        if self.user_type == "patient":
            navbar.NavBarPatient.__init__(self, master)

        self.frame = None

        self.create_notebook()

    def create_notebook(self, active_tab=0):

        self.frame = ttk.Notebook(self.master)
        self.frame.pack()

        # creating summary tab:
        f_summary = ttk.Frame(self.frame)
        self.frame.add(f_summary, text="Summary")

        # creating consultations tab:
        f_consultations = ttk.Frame(self.frame)
        self.frame.add(f_consultations, text="Consultations")

        # creating medications tab:
        f_medications = ttk.Frame(self.frame)
        self.frame.add(f_medications, text="Medications")

        # creating clinical history tab:
        f_clinical_history = ttk.Frame(self.frame)
        self.frame.add(f_clinical_history, text="Clinical History")

        # creating immunisations tab:
        f_immunisations = ttk.Frame(self.frame)
        self.frame.add(f_immunisations, text="Immunisations")

        # creating referrals tab:
        f_referrals = ttk.Frame(self.frame)
        self.frame.add(f_referrals, text="Referrals")

        # creating results tab:
        f_results = ttk.Frame(self.frame)
        self.frame.add(f_results, text="Results")

        self.frame.select(active_tab)

        # region SUMMARY TAB PATIENT DETAILS
        """-------------------summary tab------------------"""

        # creating frame within the summary tab:

        s_main_frame = tk.LabelFrame(f_summary)

        # creating the name of the frame based on whether user is patient or GP:
        if self.user_type == "patient":
            s_main_frame.config(text="Your Details", height=640, width=480)
        else:
            s_main_frame.config(text="Patient Details", height=640, width=480)
        s_main_frame.pack(pady=10)

        # creating the profile frame:

        s_profile_frame = tk.LabelFrame(s_main_frame)
        s_profile_frame.config(text="Profile")
        s_profile_frame.grid(row=0, column=0, columnspan=2, sticky="w")

        # name of patient:
        s_name_label = tk.Label(s_profile_frame, text="Name: ")
        s_name_label.grid(row=0, column=0, sticky="W")

        # printing the name:
        s_name_var = tk.Label(s_profile_frame, text=self.db.fetch_patient_full_name(self.person_id))
        s_name_var.grid(row=0, column=1, padx=(10, 25), sticky="W")

        # sex of patient:
        s_sex_label = tk.Label(s_profile_frame, text="Sex: ")
        s_sex_label.grid(row=1, column=0, sticky="W")

        # printing the sex of patient:
        s_sex_var = tk.Label(s_profile_frame,
                             text=self.db.fetch_patient_info_from_column(self.person_id, "gender"))
        s_sex_var.grid(row=1, column=1, padx=(10, 25), sticky="W")

        # age of patient:
        s_age_label = tk.Label(s_profile_frame, text="Age: ")
        s_age_label.grid(row=2, column=0, sticky="W")

        # printing the age of patient:
        s_age_var = tk.Label(s_profile_frame, text=self.db.fetch_patient_age(self.person_id))
        s_age_var.grid(row=2, column=1, padx=(10, 25), sticky="W")

        # creating the lifestyle characteristics frame:
        s_lifestyle_frame = tk.LabelFrame(s_main_frame)
        s_lifestyle_frame.config(text="Lifestyle Characteristics")
        s_lifestyle_frame.grid(row=0, column=2, columnspan=5, sticky="ew")

        # smoking label:
        s_smoking_label = tk.Label(s_lifestyle_frame, text="Smoking:")
        s_smoking_label.grid(row=0, column=0, sticky="W")

        # smoking variable:
        s_smoking_var = tk.Label(s_lifestyle_frame,
                                 text=self.db.fetch_patient_info_from_column(self.person_id, "smokingBehavior"))
        s_smoking_var.grid(row=0, column=1, padx=(10, 25), sticky="W")

        # alcohol label:
        s_alcohol_label = tk.Label(s_lifestyle_frame, text="Alcohol:")
        s_alcohol_label.grid(row=1, column=0, sticky="W")

        # alcohol variable:
        s_alcohol_var = tk.Label(s_lifestyle_frame,
                                 text=self.db.fetch_patient_info_from_column(self.person_id, "drinkingBehavior"))
        s_alcohol_var.grid(row=1, column=1, padx=(10, 25), sticky="W")

        # height label:
        s_height_label = tk.Label(s_lifestyle_frame, text="Height:")
        s_height_label.grid(row=0, column=2, sticky="W")

        # height variable:
        s_height_var = tk.Label(s_lifestyle_frame,
                                text=self.db.fetch_patient_info_from_column(self.person_id, "height"))
        s_height_var.grid(row=0, column=3, padx=(10, 25), sticky="W")

        # weight label:
        s_weight_label = tk.Label(s_lifestyle_frame, text="Weight:")
        s_weight_label.grid(row=1, column=2, sticky="W")

        # weight variable:
        s_weight_var = tk.Label(s_lifestyle_frame,
                                text=self.db.fetch_patient_info_from_column(self.person_id, "weight"))
        s_weight_var.grid(row=1, column=3, padx=(10, 25), sticky="W")

        # BMI label:
        s_bmi_label = tk.Label(s_lifestyle_frame, text="BMI:")
        s_bmi_label.grid(row=2, column=2, sticky="W")

        # BMI variable:
        s_bmi_var = tk.Label(s_lifestyle_frame, text=self.db.calculate_bmi(self.person_id))
        s_bmi_var.grid(row=2, column=3, padx=(10, 25), sticky="W")

        # exercise label:
        s_exercise_label = tk.Label(s_lifestyle_frame, text="Exercise:")
        s_exercise_label.grid(row=2, column=0, sticky="W")

        # exercise variable:
        s_exercise_var = self.db.fetch_patient_info_from_column(self.person_id, "exercise")
        s_exercise_var = tk.Label(s_lifestyle_frame,
                                  text=str(s_exercise_var) + " (10 is maximum intensity)")
        s_exercise_var.grid(row=2, column=1, padx=(10, 25), sticky="W")
        # endregion

        # region SUMMARY TAB TREEVIEWS
        """----SUMMARY TAB TREEVIEWS------"""

        # create allergies treeview table:
        s_allergies_frame = tk.LabelFrame(s_main_frame)
        s_allergies_frame.config(text="Allergies and adverse reactions")
        s_allergies_frame.grid(row=4, column=0, columnspan=7, sticky="EW")

        # creating the columns for the allergies treeview table:
        allergy_columns = ['date', 'description']
        allergy_tree = ttk.Treeview(s_allergies_frame, column=allergy_columns,
                                    show='headings', height=3, selectmode="none")
        allergy_tree.column('date', width=100, anchor="center")
        allergy_tree.column('description', width=470)

        # Creating the column headings for the allergies treeview table:
        allergy_tree.heading("#1", text="Date")
        allergy_tree.heading("#2", text="Allergy")
        allergy_tree.pack()

        # inserting data into the allergies treeview table:
        allergy_rows = self.db.fetch_all_query(f"""SELECT date(date), description 
                                                    FROM AllergiesAndAdverse 
                                                    WHERE patientID  = {self.person_id}""")
        for row in allergy_rows:
            allergy_tree.insert("", tk.END, values=row)

        # create medication treeview table:
        s_medication_frame = tk.LabelFrame(s_main_frame)
        s_medication_frame.config(text="Current medication")
        s_medication_frame.grid(row=5, column=0, columnspan=7, sticky="ew")

        # creating the columns for the medication treeview table:
        medication_columns = ['date', 'prescription']
        medication_tree = ttk.Treeview(s_medication_frame, column=medication_columns,
                                       show='headings', height=3, selectmode="none")
        medication_tree.column("date", width=100, anchor="center")
        medication_tree.column("prescription", width=470)

        # Creating the column headings for the medication treeview table:
        medication_tree.heading('#1', text='Date')
        medication_tree.heading('#2', text='Prescription')
        medication_tree.pack(fill='x')

        # inserting data into the medication treeview table:
        medication_rows = self.db.fetch_all_query(f"""SELECT date, treatment 
                                                    FROM Prescriptions 
                                                    WHERE patientID  = {self.person_id}""")
        for row in medication_rows:
            medication_tree.insert("", tk.END, values=row)

        # create clinical_prob treeview table:
        s_clinical_prob_frame = tk.LabelFrame(s_main_frame)
        s_clinical_prob_frame.config(text="Active or significant clinical problems")
        s_clinical_prob_frame.grid(row=6, column=0, columnspan=7, sticky="ew")

        # creating the columns for the clinical_prob treeview table:
        clinical_prob_columns = ['date', 'description']
        clinical_prob_tree = ttk.Treeview(s_clinical_prob_frame, column=clinical_prob_columns,
                                          show='headings', height=3, selectmode="none")
        clinical_prob_tree.column('date', width=100, anchor="center")
        clinical_prob_tree.column('description', width=470)

        # creating column headings for the clinical_prob treeview table:
        clinical_prob_tree.heading("#1", text="Date")
        clinical_prob_tree.heading("#2", text="Diagnosis")
        clinical_prob_tree.pack()

        # inserting data into the clinical_prob treeview table:
        clinical_prob_rows = self.db.fetch_all_query(f"""SELECT date(date), diagnosis 
                                                        FROM Diagnoses 
                                                        WHERE patientID  = {self.person_id}""")
        for row in clinical_prob_rows:
            clinical_prob_tree.insert("", tk.END, values=row)

        # create recent_con treeview table:
        s_recent_con_frame = tk.LabelFrame(s_main_frame)
        s_recent_con_frame.config(text="Recent Consultations")
        s_recent_con_frame.grid(row=7, column=0, columnspan=7, sticky="ew")

        # creating the columns for the recent_con treeview table:
        recent_con_columns = ['date', 'GP']
        recent_con_tree = ttk.Treeview(s_recent_con_frame, column=recent_con_columns,
                                       show='headings', height=3, selectmode="none")
        recent_con_tree.column('date', width=100, anchor="center")
        recent_con_tree.column('GP', width=470)

        # creating column headings for the clinical_prob treeview table:
        recent_con_tree.heading("#1", text="Date")
        recent_con_tree.heading("#2", text="GP")
        recent_con_tree.pack()

        # inserting data into the clinical_prob treeview table:
        recent_con_rows = self.db.retrieve_gp_appointments(self.person_id)
        for row in recent_con_rows:
            recent_con_tree.insert("", tk.END, values=row)

        # create lab_res treeview table:
        s_lab_res_frame = tk.LabelFrame(s_main_frame)
        s_lab_res_frame.config(text="Recent lab results and health assessments")
        s_lab_res_frame.grid(row=8, column=0, columnspan=7, sticky="ew")

        # creating the columns for the lab_res treeview table:
        lab_res_columns = ['date', 'result']
        lab_res_tree = ttk.Treeview(s_lab_res_frame, column=lab_res_columns,
                                    show='headings', height=3, selectmode="none")
        lab_res_tree.column('date', width=100, anchor="center")
        lab_res_tree.column('result', width=470)

        # creating column headings for the lab_res treeview table:
        lab_res_tree.heading("#1", text="Date")
        lab_res_tree.heading("#2", text="Description")
        lab_res_tree.pack()

        # inserting data into the clinical_prob treeview table:
        lab_res_rows = self.db.fetch_all_query(f"""SELECT date(date), result
                                                        FROM Labs 
                                                        WHERE patientID  = {self.person_id}""")
        for row in lab_res_rows:
            lab_res_tree.insert("", tk.END, values=row)

        """-------------CREATING HISTORY TABS----------------"""

        # defining columns for the consultation frame:
        cons_frame_tree_columns = ['Date', 'Patient Problem', 'Notes', 'Management', 'Next Follow']
        cons_frame_table_columns = "appointmentID, dateTime, patientProblem, notes, management, followup"
        # creating consultation frame:
        self.create_history_frame("consultations_frame", f_consultations, "con_tree", cons_frame_tree_columns,
                                  "Appointments", cons_frame_table_columns)

        # defining columns for the medications frame:
        med_tree_columns = ["Date", "Treatment", "Prescription"]
        med_table_columns = "prescriptionID, date, treatment, description"
        # creating prescritpion frame:
        self.create_history_frame("medications_frame", f_medications, "med_tree", med_tree_columns,
                                  "Prescriptions", med_table_columns)

        # defining columns for the clinical history frame:
        clin_his_tree_columns = ["Date", "Diagnosis", "Description", "Ongoing?"]
        clin_his_table_columns = "appointmentID, date, diagnosis, description, ongoing"
        # creating clinical history frame:
        self.create_history_frame("clin_his_frame", f_clinical_history, "clin_his_tree",
                                  clin_his_tree_columns, "Diagnoses", clin_his_table_columns)

        # defining columns for immunisations:
        immun_tree_columns = ["Date", "Vaccinations"]
        immun_table_columns = "immunisationID, date, immunisation"
        # creating immunisations frame:
        self.create_history_frame("immunisation_frame", f_immunisations, "immun_tree",
                                  immun_tree_columns, "Immunisations", immun_table_columns)

        # defining columns for referrals:
        referrals_tree_columns = ["Date", "department", "notes"]
        referrals_table_columns = "referralID, date, department, referralNotes"
        # creating referrals frame:
        self.create_history_frame("referral_frame", f_referrals, "referral_tree",
                                  referrals_tree_columns, "Referral", referrals_table_columns)

        # defining columns for results:
        results_tree_columns = ["Date", "Test", "Results"]
        results_table_columns = "labID, date, test, result"
        # creating labs frame:
        self.create_history_frame("results_frame", f_results, "results_tree",
                                  results_tree_columns, "Labs", results_table_columns)

    def create_history_frame(self, name_of_child_frame, name_of_parent_frame, tree_frame, tree_columns, table,
                             table_columns):

        # adding instructions
        if self.user_type == "patient":
            instruction_text = "Double click on a record to expand it"
        else:
            instruction_text = "Double click on a record to expand it and make modifications."

        instruction = tk.Label(name_of_parent_frame,
                               text=instruction_text)
        instruction.pack(pady=(10, 0))

        name_of_child_frame = tk.LabelFrame(name_of_parent_frame)
        name_of_child_frame.config(text="History")
        name_of_child_frame.pack(pady=10, fill="both", expand=True)

        tree_frame = ttk.Treeview(name_of_child_frame, column=tree_columns, show='headings',
                                  height=28)
        all_cols = table_columns.split(",")
        id_column = all_cols[0]
        pass_cols = all_cols[1:]
        tree_frame.bind("<Double-1>", lambda event, tree=tree_frame, table=table: self.create_popup(event, tree, table,
                                                                                                    id_column,
                                                                                                    pass_cols))
        for i in tree_columns:
            tree_frame.column(i, width=100, anchor="center", stretch=tk.YES)
        column_heading = 1
        for i in tree_columns:
            nr_column = '#' + str(column_heading)
            tree_frame.heading(nr_column, text=i)
            column_heading += 1
        tree_frame.pack(fill='both')

        # retrieving the name of the date column to use in the query below:
        date_column = all_cols[1]

        row_of_rows = self.db.fetch_all_query(f"""SELECT {table_columns}
                                                        FROM {table}
                                                        WHERE patientID  = {self.person_id}
                                                        AND {date_column} < date('now')""")
        for row in row_of_rows:
            tree_frame.insert("", tk.END, row[0], values=row[1:])

    def create_popup(self, event, tree, table, id_column, pass_cols):  # !!!!! new code added by Jetsun
        """
        Creates pop-up and autoloads fields based on row clicked on, you must ensure correct inputs passed in
        :param event: User click on treeview row
        :param tree: the name of tree view attribute e.g. (self.cons_frame_tree)
        :param table: name of database table that treeview is pulling data from
        :param id_column: id of columns
        :param id_column: columns to pass in db
        :return: pop-up with editable fields filled with row data and labelled with treeview column names
        """
        row_id = tree.identify_row(event.y)

        # check that the user has not clicked on empty space, and create pop-up window:
        if row_id != "":
            self.popup = tk.Tk()

            # name the window based on whether user is patient or GP:
            if self.user_type == "patient":
                self.popup.wm_title('Djekiin Health: View Your Records')
            else:
                self.popup.wm_title('Djekiin Health: Update Patient Records')

            self.popup.wm_iconbitmap('images/djekiin_logo.ico')
            column_list = []
            text_list = []
            for x in range(len(tree.item(item=row_id)['values'])):
                column_list.append(tree.column(x, option='id'))
                column_label = tk.Label(self.popup, text=tree.heading(x)['text'])
                column_label.pack(side="top", anchor='w', padx=20, pady=(15, 0))
                info_box = tk.Text(self.popup, width=60, height=5)
                text_list.append(info_box)
                info_box.pack(side="top", padx=20, pady=(0, 10))
                info_box.insert("insert", tree.item(item=row_id)['values'][x], 'grey')
            if not self.user_type == "patient":
                submit_button = tk.Button(self.popup, text="Update",
                                          command=lambda: self.popup_submit(event, pass_cols, table,
                                                                            row_id, text_list,
                                                                            id_column))
                submit_button.pack(side="top", anchor='e', padx=20, pady=10)
            self.popup.mainloop()

    def popup_submit(self, event, columns, table, row_id, text_list, id_column):
        """
        Submits update query based on edits to popup text feilds. Create popup function creates input values,
        which means you don't need to worry about setting these
        :param event: clicking update button
        :param columns: treeview column names
        :param table: database table name
        :param row_id: id of treeview row, aligns with primary key
        :param id_column: id of column in db
        :param text_list: list of textboxes in pop-up (so function knows which textbox to pull updated text from)
        :return: sends update query to
        """
        db = SqliteQueries("database.db")
        entry_values = []
        for i in range(len(text_list)):
            entry_values.append(text_list[i].get(0.0, "end"))
        db.update(table, columns, tuple(entry_values), '%s = %s' % (id_column, str(row_id)))

        # destroying popup
        self.popup.destroy()
        # taking note of the tab id
        tab_id = self.frame.index(self.frame.select())

        # destroying the notebook
        self.frame.destroy()

        # recreating the notebook with new values
        self.create_notebook(tab_id)


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health: Patient')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        PatientRecord(root, 10, "gp")
        root.mainloop()


    main()
