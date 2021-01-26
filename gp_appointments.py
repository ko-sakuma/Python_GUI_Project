import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import navbar
from tkcalendar import Calendar
from datetime import date
import datetime
import gl
import email_functions


class SqliteQueries:

    def __init__(self, database_location):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    def execute(self, query, data):
        self.c.execute(query, data)
        self.conn.commit()
        return self.c

    def fetch_all_appointments(self, doctor_id):
        self.c.execute(f"SELECT appointmentID, patientProblem, dateTime, status "
                       f"FROM Appointments "
                       f"WHERE  doctorID = '{doctor_id}'")
        records = self.c.fetchall()
        return records

    def fetch_day_appointments(self, selected_date, doctor_id):
        """
        :param selected_date: selected day on calendar to query for appts
        :param doctor_id: session id of logged in dr
        :return: records of appointments on selected date
        """
        self.c.execute(f"SELECT a.appointmentID, a.patientID, strftime('%H:%M', a.dateTime) AS Time, p.firstName, "
                       f"p.lastName, a.status "
                       f"FROM Appointments a, Patients p "
                       f"WHERE strftime('%Y-%m-%d', a.dateTime) = '{selected_date}' AND doctorID = '{doctor_id}'"
                       f" AND a.patientID = p.userID")
        records = self.c.fetchall()
        return records

    def update(self, table_entered, columns, data, conditionals):
        """
        :param table_entered:  table (and column names if required) in db
        :param columns: !!!must be a tuple even if single column!!! columns to update in db
        :param data: data to update record with
        :param conditionals: set which records you want to update
        :return: inserts new values into record
        :return:
        """

        # Prepares column update expression with placeholder ? for SET part of query
        columns_to_update = ""
        for x in columns:
            columns_to_update += ', ' + ('%s = ?' % x)
        columns_to_update = columns_to_update[2:]

        # Returns update query query
        return self.execute("UPDATE %s SET %s WHERE %s" % (table_entered, columns_to_update, conditionals), data)

    def get_email(self, appt_id):
        self.c.execute(f"Select email from Patients p, Appointments a where p.userID=a.patientID and a.appointmentID={appt_id} ")
        records = self.c.fetchall()
        return "{0}".format(records[0][0])


class GpAppointment(navbar.NavBarGP):

    def create_buttons(self, event):
        """
        Creates pop-up and autoloads fields based on row clicked on, you must ensure correct inputs passed in
        :param event: User click on treeview row
        :return: pop-up with editable fields filled with row data and labelled with treeview column names
        """
        # Destroy existing buttons or instructions
        self.instructions_label.destroy()
        self.r_buttons_frame.destroy()

        # Establish row values (hidden appt id and patient id)
        row_id = self.tree.focus().split()
        row_entries = self.tree.item(item=row_id)['values']
        # Not confirmed appt buttons
        if row_entries[3] == "Not confirmed":
            self.r_buttons_frame = tk.Frame(self.actions_frame)
            self.r_buttons_frame.pack()

            # Confirm appt button
            tk.Button(self.r_buttons_frame, text="Confirm", command=lambda: self.submit_confirmation(event, row_id[0]),
                      fg=self.color["NHS_Blue"], bg=self.color["white"]).pack(side="left", padx=10, pady=(5, 10))

            # Cancel appt button
            tk.Button(self.r_buttons_frame, text="Cancel", command=lambda: self.submit_cancellation(event, row_id[0]),
                      fg=self.color["NHS_Red"], bg=self.color["white"]).pack(side="right", padx=10, pady=(5, 10))

        # Button and instructions based on appt status
        elif row_entries[3] == "Confirmed":
            self.r_buttons_frame = tk.Frame(self.actions_frame)
            self.r_buttons_frame.pack()

            # Opens patient record
            tk.Button(self.r_buttons_frame, text="Patient record", command=lambda: self.open_patient_record(row_id[1]),
                      fg=self.color["NHS_Blue"], bg=self.color["white"]).pack(side="left", padx=5, pady=(5, 10))

            # Opens consultation form
            tk.Button(self.r_buttons_frame, text="Consultation form", command=lambda:
                      self.open_consultation_form(row_id[0], self.doctor_id, row_id[1]), fg=self.color["NHS_Blue"],
                      bg=self.color["white"]).pack(side="left", padx=5, pady=(5, 10))

            # Cancels patient appointment
            tk.Button(self.r_buttons_frame, text="Cancel", command=lambda: self.submit_cancellation(event, row_id[0]),
                      fg=self.color["NHS_Red"], bg=self.color["white"]).pack(side="right", padx=5, pady=(5, 10))

        elif row_entries[3] == "Attended":
            self.instructions_label = tk.Label(self.actions_frame, text='This appointment was attended')
            self.instructions_label.pack()

        elif row_entries[3] == "Missed":
            self.instructions_label = tk.Label(self.actions_frame, text='This appointment was missed')
            self.instructions_label.pack()

        else:
            self.instructions_label = tk.Label(self.actions_frame, text='This appointment has been cancelled')
            self.instructions_label.pack()

    def submit_confirmation(self, event, appt_id):
        """
        Sets appointment in db to confirmed
        :param event: click on cancellation button
        :param appt_id: appointment number
        :return: Updates appointment status to cancelled
        """
        self.db.update('Appointments', ('status',), ("Confirmed",), 'appointmentID = %s' % str(appt_id))
        messagebox.showinfo("Appointment update", "Appointment confirmed successfully.")
        self.show_appointments(event)

    def submit_cancellation(self, event, appt_id):
        """
        Sets appointment in db to cancelled
        :param event: click on cancellation button
        :param appt_id: appointment number
        :return: Updates appointment status to cancelled
        """
        self.db.update('Appointments', ('status',), ("Cancelled",), 'appointmentID = %s' % str(appt_id))
        messagebox.showinfo("Appointment update", "Appointment cancelled successfully.")
        self.show_appointments(event)

        receiver_email = self.db.get_email(appt_id)
        print(receiver_email)
        message = f"""\
                                   Subject: Your Appointment has been cancelled!

                                   This email is to confirm that your appointment has been cancelled."""
        email_functions.send_email(receiver_email, message)


    @staticmethod
    def open_consultation_form(appointment_id, doctor_id, patient_id):
        """
        Opens consultation form
        :param appointment_id: database id of appt
        :param doctor_id: database id of logged in dr
        :param patient_id: database if of selected patient
        :return: consultation form
        """
        c_form = tk.Toplevel()
        import gp_consultation_form
        gp_consultation_form.CFormInterface(c_form, appointment_id, doctor_id, patient_id)
        c_form.mainloop()

    @staticmethod
    def open_patient_record(patient_id):  # !!!!!Need to be updated with final patient record page name
        """
        Opens consultation form
        :param patient_id: id of patient attending appointment
        :return: consultation form
        """
        p_record = tk.Toplevel()
        p_record.wm_title('Djekiin Health: Patient Records')
        p_record.wm_iconbitmap('images/djekiin_logo.ico')

        import patient_my_record
        patient_my_record.PatientRecord(p_record, patient_id, "gp")
        p_record.mainloop()

    def __init__(self, master, doctor_id):

        # call up the menu bar items:
        super().__init__(master)

        self.master = master
        self.frame = tk.Frame(self.master)

        # Set page details
        self.doctor_id = doctor_id
        self.date = date.today()

        # set page color dictionary
        self.color = {"nero": "#252726", "white": "#FFFFFF", "NHS_Blue": "#005EB8", "NHS_DarkBlue": "#003087",
                      "NHS_BrighBlue": "#0072CE", "NHS_LightBlue": "#41B6E6", "NHS_AquaBlue": "#00A9CE",
                      "NHS_Yellow": "#FFB81C", "NHS_Red": "#8A1538", "NHS_Black": "#231f20", "NHS_DarkGrey": "#425563",
                      "NHS_MidGrey": "#768692", "NHS_PaleGrey": "#E8EDEE"}

        # set page db query object
        self.db = SqliteQueries('database.db')

        # retrieve GP's appts for calendar overview
        self.booked_appts = self.db.fetch_all_appointments(self.doctor_id)

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
        self.columns = ["dateTime", "firstName", "lastName", "status"]
        self.tree = ttk.Treeview(self.result_frame, column=self.columns, show="headings",
                                 selectmode="browse", height=10)

        self.tree.heading("#1", text="Time")
        self.tree.heading("#2", text="First Name")
        self.tree.heading("#3", text="Last Name")
        self.tree.heading("#4", text='Status')
        self.tree.column("#1", width=8, anchor="center")
        self.tree.column("#2", width=40, anchor="center")
        self.tree.column("#3", width=40, anchor="center")
        self.tree.column("#4", width=50, anchor="center")
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

        # Select appointment instructions
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

        # Fetches appointments for selected day
        records = self.db.fetch_day_appointments(self.date, self.doctor_id)

        # Generates the tree
        for record in records:
            self.tree.insert("", tk.END, (record[0], record[1]), values=record[2:])

        # Assigns correct messages around selecting appointments
        if records == []:
            self.instructions_label = tk.Label(self.actions_frame, text='You have no appointments on this date\n\n'
                                                                        'Select highlighted dates on the calendar')
        else:
            self.instructions_label = tk.Label(self.actions_frame, text='Select appointment to see actions')

        self.instructions_label.pack()


# Allows page to be opened directly from .py file with placeholder userID
if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.wm_title('Djekiin Health: GP')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.resizable(False, False)
        gl.main_window = root
        doctor_id = 10
        GpAppointment(root, doctor_id)
        root.mainloop()


    main()
