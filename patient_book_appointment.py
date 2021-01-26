import tkinter as tk
from tkinter import ttk
import sqlite3
import navbar
from tkcalendar import Calendar
import datetime
from datetime import date
import email_functions
from tkinter import messagebox


class SqliteQueries:
    def __init__(self, database_location):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    def execute(self, query, data):
        self.c.execute(query, data)
        self.conn.commit()
        return self.c

    def fetch_all_slot_times(self):
        """
        :return: returns all available slots for practice
        """
        self.c.execute(f"SELECT startTime "
                       f"FROM Slots ")
        records = self.c.fetchall()
        return records

    def fetch_day_slots(self, selected_date):
        """
        :param selected_date: date picked on calendar
        :return: slot on selected date
        """
        self.c.execute(f"SELECT a.startTime, a.doctorID, strftime('%H:%M', a.startTime) AS Time, "
                       f"('Dr ' || firstName || ' ' || lastName) AS doctor "
                       f"FROM Slots a, Staff b "
                       f"WHERE strftime('%Y-%m-%d', a.startTime) = '{selected_date}' AND a.doctorID = b.userID")
        records = self.c.fetchall()
        return records

    def fetch_gp_slots(self, selected_date, doctor_name):
        """
        :param selected_date: date picked on calendar
        :param doctor_name: name of doctor to query appt slots
        :return: slot on selected date
        """
        self.c.execute(f"SELECT a.startTime, a.doctorID, strftime('%H:%M', a.startTime) AS Time, "
                       f"('Dr ' || firstName || ' ' || lastName) AS doctor "
                       f"FROM Slots a, Staff b "
                       f"WHERE strftime('%Y-%m-%d', a.startTime) = '{selected_date}' AND a.doctorID = b.userID "
                       f"AND b.firstName = '{doctor_name[0]}' AND b.lastName = '{doctor_name[1]}' ")
        records = self.c.fetchall()
        return records

    def insert(self, table_entered, data):
        """
        :param table_entered: table (and column names if required) in db
        :param data: data to include in new record
        :return: inserts new record in table
        """
        # Automatically updates placeholder '?' to ensure security
        return self.execute("INSERT INTO %s VALUES (%s)" % (table_entered, ", ".join('?' * len(data))), data)

    def delete_slots(self, start_time):
        """
        :param start_time: date of slot to delete
        :return: deletes availability slot
        """
        # Automatically updates placeholder '?' to ensure security
        return self.execute("DELETE FROM 'Slots' WHERE startTime = '%s' "
                            % start_time, "")

    def delete_gp_slots(self, start_time, doctor_id):
        """
        :param start_time: time of slot to delete
        :param doctor_id: id of doctor to delete specifc dr slot
        :return: deletes specific dr appt slot in db
        """
        print(str(start_time), doctor_id)
        # Automatically updates placeholder '?' to ensure security
        return self.execute("DELETE FROM 'Slots' WHERE startTime = '%s' "
                            "AND %s = doctorID" % (str(start_time), doctor_id), "")

    def get_email(self, patient_id):
        self.c.execute(f"Select email from Patients where userID= {patient_id}")
        records = self.c.fetchall()
        return "{0}".format(records[0][0])


class PatientAppointments(navbar.NavBarPatient):  # menu_bar.menu_bar

    def create_buttons(self, event):
        """
        Creates pop-up and autoloads fields based on row clicked on, you must ensure correct inputs passed in
        :param event: User click on treeview row
        :return: pop-up with editable fields filled with row data and labelled with treeview column names
        """
        # Destroy existing buttons or instructions
        self.instructions_label.destroy()
        self.r_buttons_frame.destroy()

        # Establish row values
        row_id = self.tree.focus()

        # book  appointment button
        self.r_buttons_frame = tk.Frame(self.actions_frame)
        self.r_buttons_frame.pack()
        tk.Button(self.r_buttons_frame, text="Book", command=lambda:
                  self.book_appointment(event, row_id[1:20], self.patient_id, row_id[21:]), fg=self.color["NHS_Blue"],
                  bg=self.color["white"]).pack(side="right", padx=10, pady=(5, 10))

    def book_appointment(self, event, start_time, patient_id, doctor_id):
        """
        Creates appointment and removes slot
        :param event: click on book appointment button
        :param start_time: appointment start time
        :param doctor_id: doctor id number
        :param patient_id: patient id number
        :return: Book slot and removes it from slot db
        """
        self.db.insert('Appointments (dateTime, status, patientID, doctorID)',
                       (start_time, 'Not confirmed', patient_id, doctor_id))

        self.db.delete_gp_slots(start_time, doctor_id)
        self.show_appointments("")
        messagebox.showinfo("Appointment booked successfully!",
                            "Your appointment has been successfully booked. You will receive a confirmation email")
        receiver_email = self.db.get_email(patient_id)

        message = f"""\
                   Subject: Your Appointment has been confirmed!

                   This email is to confirm that your appointment has been scheduled for {start_time}."""
        email_functions.send_email(receiver_email, message)

    def __init__(self, master, patient_id):

        # call up the menu bar items:
        super().__init__(master)

        self.master = master
        self.frame = tk.Frame(self.master)

        # Set page details
        self.patient_id = patient_id
        self.date = date.today()

        # set page color dictionary
        self.color = {"nero": "#252726", "white": "#FFFFFF", "NHS_Blue": "#005EB8", "NHS_DarkBlue": "#003087",
                      "NHS_BrighBlue": "#0072CE", "NHS_LightBlue": "#41B6E6", "NHS_AquaBlue": "#00A9CE",
                      "NHS_Yellow": "#FFB81C", "NHS_Red": "#8A1538", "NHS_Black": "#231f20", "NHS_DarkGrey": "#425563",
                      "NHS_MidGrey": "#768692", "NHS_PaleGrey": "#E8EDEE"}

        # Sets db object
        self.db = SqliteQueries('database.db')

        # retrieve slot_times for calendar overview
        self.available_slots = self.db.fetch_all_slot_times()

        # create calendar frame
        self.calendar_frame = tk.Frame(self.frame)
        self.calendar_frame.grid(row=0, pady=10, padx=30)

        # create calendar
        self.calendar = Calendar(self.calendar_frame, font="Arial 15", selectmode='day', cursor="hand2",
                                 showweeknumbers=False, year=int(self.date.strftime("%Y")),
                                 month=int(self.date.strftime("%m")), day=int(self.date.strftime("%d")),
                                 background=self.color["NHS_Blue"], foreground=self.color["NHS_Yellow"],
                                 headersforeground=self.color["NHS_Black"], normalforeground=self.color["NHS_DarkGrey"],
                                 weekendforeground=self.color["NHS_MidGrey"], selectforeground=self.color["NHS_Yellow"])
        self.calendar.pack(fill="both", expand=True, padx=5, pady=(10, 5))
        self.calendar.bind('<<CalendarSelected>>', self.show_appointments)
        self.calendar.tag_config("grey", background=self.color["NHS_LightBlue"], foreground=self.color["NHS_DarkBlue"])

        # Attempts to update available slots
        # noinspection PyBroadException
        try:
            for slot_time in self.available_slots:
                # delete slots that are occurring before current date
                if datetime.datetime.strptime(slot_time[0], '%Y-%m-%d %H:%M:%S') < datetime.datetime.now():
                    self.db.delete_slots(slot_time[0])

                # highlights days with appointments
                Calendar.calevent_create(self.calendar, datetime.datetime.strptime(slot_time[0], '%Y-%m-%d %H:%M:%S'),
                                         text="You have appointments on this day", tags="grey")
        except Exception:
            print("Calendar did not update statuses before date")

        # create doctor drop down filter
        self.filter_instruction = tk.StringVar()
        self.filter_instruction.set('Select doctor')
        self.dr_dropdown = ttk.Combobox(self.calendar_frame, textvariable=self.filter_instruction,
                                        postcommand=self.get_doctors)
        self.dr_dropdown.pack(side="right", anchor='e', padx=(5, 0))
        self.dr_dropdown.bind("<<ComboboxSelected>>", self.show_appointments)

        # create result frame
        self.result_frame = tk.Frame(self.frame)
        self.result_frame.grid(row=2, pady=(10, 0), padx=30)

        # create treeview columns
        self.columns = ["dateTime", "doctor"]
        self.tree = ttk.Treeview(self.result_frame, column=self.columns, show="headings",
                                 selectmode="browse", height=10)

        self.tree.heading("#1", text="Time")
        self.tree.heading("#2", text="Doctor")
        self.tree.column("#1", width=10, anchor="center")
        self.tree.column("#2", width=150, anchor="center")
        self.tree.grid(row=2, column=0, padx=10, ipadx=100)

        # Add double click select function
        self.tree.bind('<<TreeviewSelect>>', self.create_buttons)

        # Actions canvas
        self.actions_frame = tk.Frame(self.frame, height=60, width=300)
        self.actions_frame.grid(row=3)
        self.actions_frame.configure(height=self.actions_frame["height"], width=self.actions_frame["width"])
        self.actions_frame.pack_propagate(False)

        # Action buttons frame
        self.r_buttons_frame = tk.Frame(self.actions_frame)
        self.r_buttons_frame.pack()

        # Select instructions
        self.instructions_label = tk.Label(self.actions_frame, text='Select a date and click show appointments')
        self.instructions_label.pack()

        self.frame.pack()

    def get_doctors(self):
        """
        :return: List of doctors for drop down filter
        """
        doctors = self.db.fetch_day_slots(self.date)
        self.dr_dropdown["values"] = self.filter_instruction
        doc_list = []
        for doctor in doctors:
            if doctor[3] not in doc_list:
                doc_list.append(doctor[3])
        self.dr_dropdown["values"] = doc_list

    def show_appointments(self, event):
        """
        :return: Tree view list of available appointments
        """
        # Attempts to delete existing labels and buttons
        try:
            self.instructions_label.destroy()
            self.r_buttons_frame.destroy()
        except AttributeError:
            print("Refresh widget exception")

        # Deletes current appts in tree
        self.tree.delete(*self.tree.get_children())

        # Gets calendar date session
        self.date = str(self.calendar.selection_get())

        # Fetches the appointments
        if self.dr_dropdown.get() != 'Select doctor':
            doctor_name = self.dr_dropdown.get().split()
            del doctor_name[0]

            records = self.db.fetch_gp_slots(self.date, doctor_name)

        else:
            records = self.db.fetch_day_slots(self.date)
            self.dr_dropdown.set('Select doctor')

        # Generates the tree
        for record in records:
            self.tree.insert("", tk.END, (record[0], record[1]), values=record[2:])

        if records == []:
            self.instructions_label = tk.Label(self.actions_frame, text='There are no available '
                                                                        'appointments on this date')
            self.dr_dropdown.set('Select doctor')
        else:
            self.instructions_label = tk.Label(self.actions_frame, text='Select appointment to book')

        self.instructions_label.pack()


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health: Patient')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        patient_id = 1
        PatientAppointments(root, patient_id)
        root.mainloop()


    main()
