import tkinter as tk
from tkinter import messagebox
import sqlite3
from urllib.request import urlopen
from urllib.parse import quote
import json
from datetime import date

# Set API addressing for the snomed-ct database (used by current NHS emr systems.
# To use API on Mac the latest python cerificates must be installed
# which can be done by going to Applications>Python>Install Certificates.command
baseUrl = 'https://browser.ihtsdotools.org/snowstorm/snomed-ct'
edition = 'MAIN'
version = '2019-07-31'


class SqliteQueries:  # to be moved to sql_query module
    def __init__(self, database_location):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    def execute(self, query, data):
        """
        :param query: sql passthrough query
        :param data: data for query
        :return: connects to sql db and does query
        """
        self.c.execute(query, data)
        self.conn.commit()
        return self.c

    def insert(self, table_entered, data):
        """
        :param table_entered: table (and column names if required) in db
        :param data: data to include in new record
        :return: inserts new record in table
        """
        # Automatically updates placeholder '?' to ensure security
        return self.execute("INSERT INTO %s VALUES (%s)" % (table_entered, ", ".join('?' * len(data))), data)

    def update(self, table_entered, columns, data, conditionals):
        """
        :param table_entered:  table (and column names if required) in db
        :param columns: !!!must be a tuple even if single column!!! columns to update in db
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

    def fetch_patient_details(self, patient_id):
        self.c.execute(f"""SELECT firstName, lastName, gender, (date('now') - dateOfBirth) as age
                           FROM Patients 
                           WHERE userID = {patient_id}""")
        patient_details = self.c.fetchone()
        return patient_details

    def fetch_departments(self):
        """
        :return: list of UCL departments
        """
        self.c.execute(f"SELECT * "
                       f"FROM Departments ")
        records = self.c.fetchall()
        return records


class CFormInterface:

    # API code for snomed db adapted from https://github.com/IHTSDO/SNOMED-in-5-minutes
    def snomed_search_menu(self, search_button, search_box, semantic_tag):
        """
        Searches the snomed ct database used by the NHS  for medical concepts
        :param search_button: gives location of button for search menu to popup
        :param search_box: the search box used where search terms were entered (must be at least 3 letters)
        :param semantic_tag: filter tag to narrow down search (disorders or treatments on this page
        :return: list of top 20 hits for search term from snomed database
        """
        search_term = search_box.get(0.0, "end-1c")
        popup_menu = tk.Menu(self.c_form_page, tearoff=0, bg=self.color['white'], fg=self.color["NHS_Black"])
        url = baseUrl + '/browser/' + edition + '/' + version + '/descriptions?term=' + quote(
            search_term) + '&conceptActive=true&semanticTag=' + quote(
            semantic_tag) + '&groupByConcept=false&searchMode=STANDARD&offset=0&limit=20'
        response = urlopen(url).read()
        data = json.loads(response.decode('utf-8'))

        if data['items']:
            for terms in data['items']:
                popup_menu.add_command(label=terms['term'], command=lambda menuterm=terms['term']:
                                       (search_box.delete(0.0, 'end-1c'), search_box.insert(0.0, chars=menuterm)))
        else:
            popup_menu.add_command(label="Search term not found")
            popup_menu.entryconfig(0, foreground=self.color["NHS_Red"])
        try:
            x = search_button.winfo_rootx()
            y = search_button.winfo_rooty()
            popup_menu.tk_popup(x, y, 0)
        finally:
            popup_menu.grab_release()

    def referral_search_menu(self, search_button, search_box):
        """
        Searches the prepopulated list of UCL specialist departments
        :param search_button: gives location of button for search menu to popup
        :param search_box: the search box used where search terms were entered (must be at least 3 letters)
        :return: list of top  hits for search term from our UCL department database
        """
        departments = self.db.fetch_departments()
        popup_menu = tk.Menu(self.c_form_page, tearoff=0, bg=self.color['white'])
        not_empty = 0
        for department in departments:
            if search_box.get(0.0, "end-1c").lower() in department[0].lower():
                popup_menu.add_command(label=department[0], command=lambda menuterm=department[0]:
                                       (search_box.delete(0.0, 'end-1c'), search_box.insert(0.0, chars=menuterm)))
                not_empty = 1
        if not_empty != 1:
            popup_menu.add_command(label="Search term not found")
            popup_menu.entryconfig(0, foreground=self.color["NHS_Red"])
        try:
            x = search_button.winfo_rootx()
            y = search_button.winfo_rooty()
            popup_menu.tk_popup(x, y, 0)
        finally:
            popup_menu.grab_release()

    @staticmethod
    def default_text(entry_field, default):
        """
        Sets default text and add functonality
        :param entry_field: the label or textbox you want to insert default text into
        :param default:
        :return:
        """

        def default_text_clear(event, arg):
            """
            Nested function that adds default text functionality
             :param event: clicking into an entry or text box to enter text
             :param arg: arg[0] the entry or textbox you have default text in (e.g. self.treatment_search).
             arg[1] the default text you have in the entry box
             :return: removes text in entry/text box if default, leaves otherwise
             """
            # checks if default text is in box when clicked on
            if arg[1] in arg[0].get(0.0, "end"):
                arg[0].delete(0.0, "end")
            arg[0].unbind('<FocusIn>')
            arg[0].bind("<FocusOut>", lambda focusout, bindings=(entry_field, default):
                        default_text_put_back(focusout, bindings))

        def default_text_put_back(event, arg):
            """
            Nested function that adds default text functionality
             :param event: clicking into another textbox from current textbox
             :param arg: arg[0] the texbox clicking away from  (e.g. self.treatment_search)
             arg[1] the default text for this box
             :return: adds text in entry/text box if textbox empty and keyboard focus leaves box
             """
            # checks if default text is in box when clicked on
            if len(arg[0].get("1.0", "end-1c")) == 0:
                arg[0].insert("insert", arg[1], 'grey')
            entry_field.bind("<FocusIn>", lambda focus_in, bindings=(entry_field, default):
                             default_text_clear(focus_in, bindings))

        # sets default text as grey
        entry_field.tag_config('grey', foreground="grey")

        entry_field.insert("insert", default, 'grey')
        entry_field.bind("<FocusIn>", lambda event, arg=(entry_field, default): default_text_clear(event, arg))

    def __init__(self, master, appointment_id, doctor_id, patient_id):
        """
        UI interface and session initialisation
        :param master: master window
        :param appointment_id:  ID of current appointment
        :param doctor_id: session ID for logged in doctor
        :param patient_id: ID of patient attending appointment
        """

        self.master = master
        self.c_form_page = tk.Frame(self.master)

        # Set page session details
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date.today()

        # Set styling dictionaries
        self.color = {"nero": "#252726", "white": "#FFFFFF", "tk_gray": "#F0F0F0",
                      "NHS_Blue": "#005EB8", "NHS_DarkBlue": "#003087", "NHS_BrightBlue": "#0072CE",
                      "NHS_LightBlue": "#41B6E6", "NHS_AquaBlue": "#00A9CE", "NHS_Red": "#8A1538",
                      "NHS_Black": "#231f20", "NHS_DarkGrey": "#425563", "NHS_MidGray": "#768692",
                      "NHS_PaleGrey": "#E8EDEE"}

        self.search_icons = {"active": tk.PhotoImage(file=r"images/actv_srch_btn.png"),
                             "disabled": tk.PhotoImage(file=r"images/disabld_srch_btn.png")}

        # create class instance for the database
        self.db = SqliteQueries('database.db')

        # create variables for followup
        self.months = tk.StringVar("")
        self.weeks = tk.StringVar("")

        # Retrieve patient details from db and set at top of page
        self.patient_details = self.db.fetch_patient_details(self.patient_id)
        self.p_details = tk.Label(self.c_form_page, text='Name: %s | Gender: %s | Age: %s'
                                                         % (self.patient_details[0] + " " + self.patient_details[1],
                                                            self.patient_details[2], self.patient_details[3]),
                                  font="TkTextFont 10")
        self.p_details.grid(row=0, column=0, padx=16, pady=(20, 5), sticky="w")

        """Assessment section-------------------------------------------------------------------"""

        # Assessment section frame:

        self.a_frame = tk.LabelFrame(self.c_form_page, text="ASSESSMENT", fg=self.color["NHS_Black"],
                                     font="TkTextFont 10 bold", bd=2, relief="solid")
        self.a_frame.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        """-----------------Problem sub-section---------------------------------------------"""

        # patient problem frame:

        self.p_frame = tk.LabelFrame(self.a_frame, text='Patient problem', font="TkTextFont 9 bold")
        self.p_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # text box for patient problem:

        self.patient_problem = tk.Text(self.p_frame, width=113, height=3, highlightbackground=self.color["tk_gray"],
                                       highlightthickness=0.5, font="TkTextFont 9")
        self.patient_problem.grid(row=0, column=0, padx=(10, 33), pady=10, sticky="w")

        self.patient_problem_scrollbar = tk.Scrollbar(self.p_frame, orient="vertical",
                                                      command=self.patient_problem.yview)
        self.patient_problem_scrollbar.grid(row=0, column=0, padx=(0, 15), pady=(10, 15), sticky="nes")

        self.patient_problem.configure(yscrollcommand=self.patient_problem_scrollbar.set)

        """-----------------Notes sub-section---------------------------------------------"""

        # notes box frame

        self.n_frame = tk.LabelFrame(self.a_frame, text='Notes', font="TkTextFont 9 bold")
        self.n_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # text box for notes:

        self.notes = tk.Text(self.n_frame, width=113, height=3, highlightbackground=self.color["tk_gray"],
                             highlightthickness=0.5, font="TkTextFont 9")
        self.notes.grid(row=0, column=0, padx=(10, 33), pady=10, sticky="w")

        self.notes_scrollbar = tk.Scrollbar(self.n_frame, orient="vertical", command=self.notes.yview)
        self.notes_scrollbar.grid(row=0, column=0, padx=(0, 15), pady=(10, 15), sticky="nes")

        self.notes.configure(yscrollcommand=self.notes_scrollbar.set)

        """Outcomes section-------------------------------------------------------------------"""

        # Outcome section frame:

        self.o_frame = tk.LabelFrame(self.c_form_page, text="OUTCOMES", fg=self.color["NHS_Black"],
                                     font="TkTextFont 10 bold", bd=2, relief="solid")
        self.o_frame.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="w")

        """-----------------Diagnosis sub-section---------------------------------------------"""

        # Diagnosis sub-section frame:

        self.d_frame = tk.LabelFrame(self.o_frame, text="Diagnosis", font="TkTextFont 9 bold")
        self.d_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        # Diagnoses search box:
        self.diag_search = tk.Text(self.d_frame, width=35, height=1, highlightbackground=self.color["tk_gray"],
                                   highlightthickness=0.5, font="TkTextFont 9")
        self.default_text(self.diag_search, "Enter at least 3 chars to search diagnoses")
        self.diag_search.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Diagnoses search button:
        self.diag_search_button = tk.Button(self.d_frame, image=self.search_icons["disabled"], state="disabled",
                                            borderwidth=0)
        self.diag_search_button.configure(command=lambda: self.snomed_search_menu(self.diag_search_button,
                                                                                  self.diag_search, 'disorder'))
        self.diag_search_button.grid(row=0, column=2, pady=10, sticky="w")

        # Search button 3 letter activation
        self.diag_search.bind("<KeyRelease>", lambda event, arg=(self.diag_search, self.diag_search_button):
                              self.search_activate(event, arg))

        # Diagnosis description box:
        self.diag_description = tk.Text(self.d_frame, height=1, width=66, highlightbackground=self.color["tk_gray"],
                                        highlightthickness=0.5, font="TkTextFont 9")
        self.default_text(self.diag_description, "Add any additional diagnostic information")
        self.diag_description.grid(row=0, column=4, padx=(45, 10), pady=10, sticky="we")

        """-----------------Management sub-section---------------------------------------------"""

        # Management label and frame

        self.m_frame = tk.LabelFrame(self.o_frame, text='Management', font="TkTextFont 9 bold")
        self.m_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 0), sticky="w")

        # Management text box

        self.management = tk.Text(self.m_frame, width=113, height=3, highlightbackground=self.color["tk_gray"],
                                  highlightthickness=0.5, font="TkTextFont 9")
        self.management.grid(row=3, column=0, padx=(10, 33), pady=(10, 15), sticky="w")

        # Management scroll bar

        self.management_scrollbar = tk.Scrollbar(self.m_frame, orient="vertical", command=self.management.yview)
        self.management_scrollbar.grid(row=3, column=0, padx=(0, 15), pady=(10, 15), sticky="nes")

        self.management.configure(yscrollcommand=self.management_scrollbar.set)

        """-----------------Treatment sub-section---------------------------------------------"""

        self.t_frame = tk.LabelFrame(self.o_frame, text="Treatment", font="TkTextFont 9 bold")
        self.t_frame.grid(row=4, column=0, padx=(10, 4), pady=10, sticky="w")

        # Treatment search

        self.treat_search = tk.Text(self.t_frame, width=50, height=1, highlightbackground=self.color["tk_gray"],
                                    highlightthickness=0.5, font="TkTextFont 9")
        self.default_text(self.treat_search, "Enter at least 3 chars to search treatments")
        self.treat_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.treat_search_button = tk.Button(self.t_frame, image=self.search_icons["disabled"], state="disabled",
                                             borderwidth=0)
        self.treat_search_button.configure(command=lambda: self.snomed_search_menu(self.treat_search_button,
                                                                                   self.treat_search, 'clinical drug'))
        self.treat_search_button.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="w")

        # Search button 3 letter activation
        self.treat_search.bind("<KeyRelease>", lambda event, arg=(self.treat_search, self.treat_search_button):
                               self.search_activate(event, arg))

        # Prescription entry:

        self.prescription = tk.Text(self.t_frame, width=50, height=3, highlightbackground=self.color["tk_gray"],
                                    highlightthickness=0.5, font="TkTextFont 9")
        self.default_text(self.prescription, "Enter prescription")
        self.prescription.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.prescription_scrollbar = tk.Scrollbar(self.t_frame, orient="vertical", command=self.management.yview)
        self.prescription_scrollbar.grid(row=1, column=0, columnspan=2, padx=(0, 25), pady=10, sticky="nes")

        self.prescription.configure(yscrollcommand=self.prescription_scrollbar.set)

        """-----------------Referral sub-section---------------------------------------------"""

        self.r_frame = tk.LabelFrame(self.o_frame, text="Referral", font="TkTextFont 9 bold")
        self.r_frame.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        # Referral search

        self.referral_search = tk.Text(self.r_frame, width=50, height=1, highlightbackground=self.color["tk_gray"],
                                       highlightthickness=0.5, font="TkTextFont 9")
        self.default_text(self.referral_search, "Enter at least 3 chars to search departments")
        self.referral_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.referral_search_button = tk.Button(self.r_frame, image=self.search_icons["disabled"], state="disabled",
                                                borderwidth=0)
        self.referral_search_button.configure(command=lambda: self.referral_search_menu(self.referral_search_button,
                                                                                        self.referral_search))
        self.referral_search_button.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="w")

        # Search button 3 letter activation
        self.referral_search.bind("<KeyRelease>", lambda event, arg=(self.referral_search, self.referral_search_button):
                                  self.search_activate(event, arg))

        # Referral notes entry:

        self.referral_notes = tk.Text(self.r_frame, width=50, height=3, highlightbackground=self.color["tk_gray"],
                                      highlightthickness=0.5, font="TkTextFont 9")
        self.default_text(self.referral_notes, "Enter referral notes")
        self.referral_notes.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.referral_notes_scrollbar = tk.Scrollbar(self.r_frame, orient="vertical", command=self.management.yview)
        self.referral_notes_scrollbar.grid(row=1, column=0, columnspan=2, padx=(0, 25), pady=10, sticky="nes")

        self.referral_notes.configure(yscrollcommand=self.referral_notes_scrollbar.set)

        """Submission section-------------------------------------------------------------------"""

        self.submission = tk.Frame(self.c_form_page, height=60, width=865)
        self.submission.grid(row=3, column=0)
        self.submission.configure(height=self.submission["height"], width=self.submission["width"])
        self.submission.pack_propagate(False)

        self.followframe = tk.Frame(self.submission)
        self.followframe.pack(side="left")

        # Set follow up
        self.followup_button = tk.Button(self.followframe, text="SET FOLLOW-UP TIME", fg=self.color["NHS_Blue"],
                                         bg=self.color["white"], font="TkTextFont 10 bold", command=self.set_follow_up)
        self.followup_button.pack(side="left")

        # Submit form button
        self.submit_button = tk.Button(self.submission, text="SUBMIT FORM", fg=self.color["NHS_Blue"],
                                       bg=self.color["white"], font="TkTextFont 10 bold", command=self.submit)
        self.submit_button.pack(side="right")
        self.c_form_page.pack()

    def set_follow_up(self):
        """
        Creates set follow up widgets
        :return: set follow up sections
        """
        self.followup_button.destroy()
        months_label = tk.Label(self.followframe, text="Months:")
        months_label.pack(side="left")
        self.months = tk.StringVar(value='00')
        months_box = tk.Spinbox(self.followframe, from_=0, to=12, textvariable=self.months)
        months_box.pack(side="left")

        weeks_label = tk.Label(self.followframe, text="  Weeks:")
        weeks_label.pack(side="left")
        self.weeks = tk.StringVar(value='00')
        weeks_box = tk.Spinbox(self.followframe, from_=0, to=4, textvariable=self.weeks)
        weeks_box.pack(side="left")

    def submit(self):
        """
        input: Submit button click
        :return: Submits form data to relevant table or returns exceptions, closes form on successful submission
        """

        # Return warning message if mandatory fields left empty
        if self.patient_problem.get(0.0, "end-1c") == "":
            return messagebox.showinfo("Form not submitted", "'Patient problem' is empty. "
                                       "\nDescribe the patient problem even if resolved.")

        elif self.notes.get(0.0, "end-1c") == "":
            return messagebox.showinfo("Form not submitted", "'Notes' cannot be left empty. "
                                       "\nDescribe the appointment even if patient problem resolved.")

        elif self.management.get(0.0, "end-1c") == "":
            return messagebox.showinfo("Form not submitted", "'Management' cannot be left empty. "
                                       "\nDescribe the management strategy or enter 'none required'")

        elif (("Enter at least 3 chars to search treatments" not in self.treat_search.get(0.0, "end-1c"))
              and ("Enter prescription" in self.prescription.get(0.0, "end-1c"))):
            return messagebox.showinfo("Form not submitted", "Treatment set but prescription empty. "
                                       "\nYou must include prescription details for your patient.")

        elif (("Enter at least 3 chars to search departments" not in self.referral_search.get(0.0, "end-1c"))
              and ("Enter referral notes" in self.referral_notes.get(0.0, "end-1c"))):
            return messagebox.showinfo("Form not submitted", "Referral set but referral notes empty. "
                                       "\nYou must include information about consultation for specialist.")
        else:
            # Check if follow-up entry made and set variable for update
            try:
                follow_up_date = self.months.get() + " months " + self.weeks.get() + " weeks"
            except AttributeError:
                follow_up_date = None

            # Updates appointment record with descriptions of consultation
            self.db.update('Appointments', ('patientProblem', 'notes', 'management', 'followup'),
                           (self.patient_problem.get(0.0, "end-1c"), self.notes.get(0.0, "end-1c"),
                            self.management.get(0.0, "end-1c"), follow_up_date),
                           'appointmentID = %s' % self.appointment_id)

            # Insert diagnosis for patient if established
            if ("Enter at least 3 chars to search diagnoses" not in self.diag_description.get(0.0, "end-1c")) \
                    and (len(self.treat_search.get(0.0, "end-1c")) != 0):
                self.db.insert('Diagnoses (date, diagnosis, description, appointmentID, patientID, doctorID, ongoing)',
                               (self.date, self.diag_search.get(0.0, "end-1c"),
                                self.diag_description.get(0.0, "end-1c"),
                                self.appointment_id, self.patient_id, self.doctor_id, "Yes"))

            # Insert prescription for patient if prescribed
            if ("Enter at least 3 chars to search treatments" not in self.treat_search.get(0.0, "end-1c")) \
                    and (len(self.treat_search.get(0.0, "end-1c")) != 0):
                self.db.insert('Prescriptions (date, treatment, description, appointmentID, patientID, doctorID)',
                               (self.date, self.treat_search.get(0.0, "end-1c"), self.prescription.get(0.0, "end-1c"),
                                self.appointment_id, self.patient_id, self.doctor_id))

            # Insert referral appointment entry if required
            if ("Enter at least 3 chars to search departments" not in self.referral_search.get(0.0, "end-1c")) \
                    and (len(self.referral_search.get(0.0, "end-1c")) != 0):
                self.db.insert('Referral (date, department, referralNotes, referringDoctorID, patientID)',
                               (self.date, self.referral_search.get(0.0, "end-1c"),
                                self.referral_notes.get(0.0, "end-1c"), self.doctor_id, self.patient_id))

            # close form after submission
            messagebox.showinfo("Success", "Form submitted successfully")
            self.master.destroy()

    def search_activate(self, event, arg):
        """
        Activates the search button when 3 letters have been entered into the search box, preventing users from
        entering 1 or 2 letter search terms which generate results too slowly
        :param event: keyboard entry into search box
        :param arg: arg[0] searchbox entry. arg[1] button for changing states
        :return: activates button if 3 letters entered to searchbox
        """
        if len(arg[0].get(0.0, "end-1c")) >= 3:
            arg[1]['state'] = 'normal'
            arg[1]['image'] = self.search_icons["active"]
        else:
            arg[1]['state'] = 'disable'
            arg[1]['image'] = self.search_icons["disabled"]


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.title('Djekiin Health: Consultation Form')
        CFormInterface(root, patient_id=10, appointment_id=9, doctor_id=10)
        root.mainloop()


    main()
