import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import navbar
from tkcalendar import Calendar
from datetime import date
import datetime
import email_functions


class SqliteQueries:
    def __init__(self, database_location):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    def execute(self, query, data):
        self.c.execute(query, data)
        self.conn.commit()
        return self.c

    def fetch_all_appointments(self, patient_id):
        self.c.execute(f"SELECT appointmentID, patientProblem, dateTime, status "
                       f"FROM Appointments "
                       f"WHERE  patientID = '{patient_id}'")
        records = self.c.fetchall()
        return records

    def fetch_day_appointments(self, selected_date, patient_id):
        self.c.execute(f"SELECT a.appointmentID, a.doctorID, a.dateTime, strftime('%H:%M', a.dateTime) AS Time, "
                       f"('Dr ' || firstNAme || ' ' || lastName) AS doctor, a.status "
                       f"FROM Appointments a, Staff s "
                       f"WHERE strftime('%Y-%m-%d', a.dateTime) = '{selected_date}' AND patientID = '{patient_id}'"
                       f" AND a.doctorID = s.userID")
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
        row_entries = self.tree.item(item=row_id)['values']

        # Not confirmed appt buttons
        if row_entries[2] == "Cancelled":
            self.instructions_label = tk.Label(self.actions_frame, text='This appointment has been cancelled')
            self.instructions_label.pack()

        elif row_entries[2] == "Attended":
            self.instructions_label = tk.Label(self.actions_frame, text='You attended this appointment')
            self.instructions_label.pack()

        elif row_entries[2] == "Missed":
            self.instructions_label = tk.Label(self.actions_frame, text='You missed this appointment \n Missing three '
                                                                        'without cancelling \n could result '
                                                                        'in a ban from our practice')
            self.instructions_label.pack()

        else:
            # Cancel patient appointment button
            self.r_buttons_frame = tk.Frame(self.actions_frame)
            self.r_buttons_frame.pack()
            tk.Button(self.r_buttons_frame, text="Cancel", command=lambda:
                      self.submit_cancellation(event, row_id[0], row_id[1], row_id[2]), fg=self.color["NHS_Red"],
                      bg=self.color["white"]).pack(side="right", padx=10, pady=(5, 10))

    def submit_cancellation(self, event, appt_id, doctor_id, appt_time):
        """
        Sets appointment in db to cancelled
        :param event: click on cancellation button
        :param appt_id: appointment number
        :param doctor_id: id of dr whose appt to cancel
        :param appt_time: time of appt to cancel
        :return: Updates appointment status to cancelled
        """
        self.db.update('Appointments', ('status',), ("Cancelled",), 'appointmentID = %s' % str(appt_id))
        self.db.insert('Slots (doctorID, startTime)', (doctor_id, appt_time))
        messagebox.showinfo("Appointment update", "Appointment cancelled successfully.")
        self.show_appointments(event)

        # Emails patient to let them know that their appointment has been cancelled
        receiver_email = self.db.get_email(self.patient_id)
        message = f"""\
                           Subject: Your Appointment has been cancelled!

                           This email is to confirm that your appointment has been cancelled."""
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

        # set page db query object
        self.db = SqliteQueries('database.db')

        # retrieve GP's appts for calendar overview
        self.booked_appts = self.db.fetch_all_appointments(self.patient_id)

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

        # highlights days with appointments
        # noinspection PyBroadException
        try:
            for appts in self.booked_appts:
                Calendar.calevent_create(self.calendar, datetime.datetime.strptime(appts[2], '%Y-%m-%d %H:%M:%S'),
                                         text="You have appointments on this day", tags="grey")

                # updates appointments from before current date as missed or attended
                # (based on if consultation form was submitted)
                if datetime.datetime.strptime(appts[2], '%Y-%m-%d %H:%M:%S') < datetime.datetime.now():
                    if appts[1] == None:

                        self.db.update('Appointments', ('status',), ("Missed",), 'appointmentID = %s'
                                       % str(appts[0]))
                    else:
                        self.db.update('Appointments', ('status',), ("Attended",), 'appointmentID = %s'
                                       % str(appts[0]))
        except Exception:
            print("Calendar did not update statuses before date")

        # create result frame
        self.result_frame = tk.Frame(self.frame)
        self.result_frame.grid(row=2, pady=(10, 0), padx=30)

        # create treeview columns
        self.columns = ["dateTime", "doctor", "status"]
        self.tree = ttk.Treeview(self.result_frame, column=self.columns, show="headings",
                                 selectmode="browse", height=10)

        self.tree.heading("#1", text="Time")
        self.tree.heading("#2", text="Doctor")
        self.tree.heading("#3", text='Status')
        self.tree.column("#1", width=10, anchor="center")
        self.tree.column("#2", width=100, anchor="center")
        self.tree.column("#3", width=30, anchor="center")
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
        self.instructions_label = tk.Label(self.actions_frame, text='Highlighted dates have appointments')
        self.instructions_label.pack()

        self.frame.pack()

    def show_appointments(self, event):

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
        records = self.db.fetch_day_appointments(self.date, self.patient_id)

        # Generates the tree
        for record in records:
            self.tree.insert("", tk.END, (record[0], record[1], record[2]), values=record[3:])

        if records == []:
            self.instructions_label = tk.Label(self.actions_frame, text='You have no appointments on this date')
        else:
            self.instructions_label = tk.Label(self.actions_frame, text='Select appointment to see actions')

        self.instructions_label.pack()


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.wm_title('Djekiin Health: Patient')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.resizable(False, False)
        patient_id = 10
        PatientAppointments(root, patient_id)
        root.mainloop()


    main()
