import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import navbar
from tkcalendar import DateEntry
from datetime import date
import gl
import datetime


class SqliteQueries:

    def __init__(self, database_location):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    def execute(self, query, data):
        self.c.execute(query, data)
        self.conn.commit()
        return self.c

    def fetch_all_slots(self, doctor_id):
        """
        :param doctor_id: id of doctor to fetch slots
        :return: slot on selected date
        """
        self.c.execute(f"SELECT a.startTime, strftime('%Y-%m-%d', a.startTime) AS Date, "
                       f"strftime('%H:%M', a.startTime) AS Time "
                       f"FROM Slots a "
                       f"WHERE a.doctorID = {doctor_id}")
        records = self.c.fetchall()
        return records

    def delete_slots(self, start_time, doctor_id):
        """
        :param start_time: time of slot to delete
        :param doctor_id: id of doctor to delete specifc dr slot
        :return: inserts new record in table
        """
        # Automatically updates placeholder '?' to ensure security
        return self.execute("DELETE FROM 'Slots' WHERE startTime = '%s' "
                            "AND %s = doctorID" % (start_time, doctor_id), "")


class GpAvailability(navbar.NavBarGP):

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

        # Book appointment button
        self.r_buttons_frame = tk.Frame(self.actions_frame)
        self.r_buttons_frame.pack()
        tk.Button(self.r_buttons_frame, text="Cancel", bg=self.color["white"],
                  fg=self.color["nero"],
                  activebackground=self.color["NHS_Blue"],
                  activeforeground=self.color["NHS_PaleGrey"],
                  command=lambda: self.cancel_slot(event, row_id, self.doctor_id)) \
            .pack(side="right", padx=10, pady=(5, 10))

    def cancel_slot(self, event, start_time, doctor_id):
        """
        Creates appointment and removes slot
        :param event: click on book appointment button
        :param start_time: appointment start time
        :param doctor_id: doctor id number
        :return: Book slot and removes it from slot db
        """
        print(start_time)
        self.db.delete_slots(start_time, doctor_id)
        self.show_appointments()

    def __init__(self, master, doctor_id):

        # Call up the menu bar items:
        super().__init__(master)

        self.master = master
        self.frame = tk.LabelFrame(self.master, text="Set availability", font="TkTextFont 10 bold")

        # Set page details
        self.doctor_id = doctor_id
        self.date = date.today()
        self.color = {"nero": "#252726", "white": "#FFFFFF",
                      "NHS_Blue": "#005EB8", "NHS_DarkBlue": "#003087", "NHS_BrighBlue": "#0072CE",
                      "NHS_LightBlue": "#41B6E6", "NHS_AquaBlue": "#00A9CE",
                      "NHS_Black": "#231f20", "NHS_DarkGrey": "#425563", "NHS_MidGray": "#768692",
                      "NHS_PaleGrey": "#E8EDEE"}

        # Sets db object
        self.db = SqliteQueries('database.db')

        # initialising start and end dictionary
        self.start_end = {}

        """Select date range section-------------------------------------------------------------------"""

        # Date range frame
        self.date_range_frame = tk.LabelFrame(self.frame, text="Select date range", font="TkTextFont 10")
        self.date_range_frame.pack(padx=10, pady=10)

        self.start_date_label = tk.Label(self.date_range_frame, text="Start date:")
        self.start_date_label.grid(row=0, column=0, padx=4, sticky="w")

        self.end_date_label = tk.Label(self.date_range_frame, text="End date:")
        self.end_date_label.grid(row=0, column=2, padx=4, sticky="w")

        # Start date drop down calendar
        self.start_date = DateEntry(self.date_range_frame, width=12, background='#005EB8', foreground='white',
                                    borderwidth=2, year=datetime.datetime.now().year,
                                    month=datetime.datetime.now().month, day=datetime.datetime.now().day,
                                    date_pattern="YYYY-MM-DD")
        self.start_date._top_cal.overrideredirect(False)

        self.start_date.grid(row=0, column=1, padx=(2, 20), pady=(10, 15))

        # End date drop down calendar
        self.end_date = DateEntry(self.date_range_frame, width=12, background='#005EB8', foreground='white',
                                  borderwidth=2, year=datetime.datetime.now().year, month=datetime.datetime.now().month,
                                  day=datetime.datetime.now().day, date_pattern="YYYY-MM-DD")
        self.end_date.grid(row=0, column=3, padx=(2, 5), pady=(10, 15))
        self.end_date._top_cal.overrideredirect(False)

        """Select shifts section-------------------------------------------------------------------"""

        # Available days and shifts frame
        self.days_shifts_frame = tk.LabelFrame(self.frame, text="Select shifts", font="TkTextFont 10")
        self.days_shifts_frame.pack()
        self.confirm = tk.Button(self.frame, text="Confirm", bg=self.color["white"],
                                 fg=self.color["nero"],
                                 activebackground=self.color["NHS_Blue"],
                                 activeforeground=self.color["NHS_PaleGrey"], command=self.confirm)
        self.confirm.pack(pady=10)
        self.availability_days_times = {}

        # Work day column labels
        self.monday = tk.Label(self.days_shifts_frame, text="Monday")
        self.monday.grid(row=0, column=1)

        self.tuesday = tk.Label(self.days_shifts_frame, text="Tuesday")
        self.tuesday.grid(row=0, column=2)

        self.wednesday = tk.Label(self.days_shifts_frame, text="Wednesday")
        self.wednesday.grid(row=0, column=3)

        self.thursday = tk.Label(self.days_shifts_frame, text="Thursday")
        self.thursday.grid(row=0, column=4)

        self.friday = tk.Label(self.days_shifts_frame, text="Friday")
        self.friday.grid(row=0, column=5)

        # Work shift row labels
        self.am_shift = tk.Label(self.days_shifts_frame, text="9:00AM - 1:00PM")
        self.am_shift.grid(row=1, column=0, sticky="w")

        self.pm_shift = tk.Label(self.days_shifts_frame, text="2:00PM - 6:00PM")
        self.pm_shift.grid(row=2, column=0, sticky="w")

        # Monday shift checkboxes
        self.monday_am = tk.StringVar(value=0)
        self.monday_am_check = tk.Checkbutton(self.days_shifts_frame, onvalue=1, variable=self.monday_am,
                                              command=lambda: self.create_times([0, ["09:00:00", "13:00:00"]],
                                                                                self.monday_am),
                                              offvalue=0)
        self.monday_am_check.grid(row=1, column=1)

        self.monday_pm = tk.StringVar(value=0)
        self.monday_pm_check = tk.Checkbutton(self.days_shifts_frame, variable=self.monday_pm, onvalue=1,
                                              offvalue=0,
                                              command=lambda: self.create_times([0, ["14:00:00", "18:00:00"]],
                                                                                self.monday_pm))
        self.monday_pm_check.grid(row=2, column=1)

        # Tuesday shift checkboxes
        self.tuesday_am = tk.StringVar(value=0)
        self.tuesday_am_check = tk.Checkbutton(self.days_shifts_frame, variable=self.tuesday_am, onvalue=1,
                                               offvalue=0,
                                               command=lambda: self.create_times([1, ["09:00:00", "13:00:00"]],
                                                                                 self.tuesday_am))
        self.tuesday_am_check.grid(row=1, column=2)

        self.tuesday_pm = tk.StringVar(value=0)
        self.tuesday_pm_check = tk.Checkbutton(self.days_shifts_frame, variable=self.tuesday_pm, onvalue=1,
                                               offvalue=0,
                                               command=lambda: self.create_times([1, ["14:00:00", "18:00:00"]],
                                                                                 self.tuesday_pm))
        self.tuesday_pm_check.grid(row=2, column=2)

        # Wednesday shift checkboxes
        self.wednesday_am = tk.StringVar(value=0)
        self.wednesday_am_check = tk.Checkbutton(self.days_shifts_frame, variable=self.wednesday_am, onvalue=1,
                                                 offvalue=0,
                                                 command=lambda: self.create_times([2, ["09:00:00", "13:00:00"]],
                                                                                   self.wednesday_am))
        self.wednesday_am_check.grid(row=1, column=3)

        self.wednesday_pm = tk.StringVar(value=0)
        self.wednesday_pm_check = tk.Checkbutton(self.days_shifts_frame, variable=self.wednesday_pm, onvalue=1,
                                                 offvalue=0,
                                                 command=lambda: self.create_times([2, ["14:00:00", "18:00:00"]],
                                                                                   self.wednesday_pm))
        self.wednesday_pm_check.grid(row=2, column=3)

        # Thursday shift checkboxes
        self.thursday_am = tk.StringVar(value=0)
        self.thursday_am_check = tk.Checkbutton(self.days_shifts_frame, variable=self.thursday_am, onvalue=1,
                                                offvalue=0,
                                                command=lambda: self.create_times([3, ["09:00:00", "13:00:00"]],
                                                                                  self.thursday_am))
        self.thursday_am_check.grid(row=1, column=4)

        self.thursday_pm = tk.StringVar(value=0)
        self.thursday_pm_check = tk.Checkbutton(self.days_shifts_frame, variable=self.thursday_pm, onvalue=1,
                                                offvalue=0,
                                                command=lambda: self.create_times([3, ["14:00:00", "18:00:00"]],
                                                                                  self.thursday_pm))
        self.thursday_pm_check.grid(row=2, column=4)

        # Friday shift checkboxes
        self.friday_am = tk.StringVar(value=0)
        self.friday_am_check = tk.Checkbutton(self.days_shifts_frame, variable=self.friday_am, onvalue=1,
                                              offvalue=0,
                                              command=lambda: self.create_times([4, ["09:00:00", "13:00:00"]],
                                                                                self.friday_am))
        self.friday_am_check.grid(row=1, column=5)

        self.friday_pm = tk.StringVar(value=0)
        self.friday_pm_check = tk.Checkbutton(self.days_shifts_frame, variable=self.friday_pm, onvalue=1,
                                              offvalue=0,
                                              command=lambda: self.create_times([4, ["14:00:00", "18:00:00"]],
                                                                                self.friday_pm))
        self.friday_pm_check.grid(row=2, column=5)

        """See current availability slots-------------------------------------------------------------------"""

        # Set see current availability frame
        self.current_availability_frame = tk.Label(self.frame, text="Current availability", font="TkTextFont 10")
        self.current_availability_frame.pack(anchor="w", padx=(15, 0), pady=(10, 0))

        # Create treeview columns
        self.columns = ["Date", "Time"]
        self.tree = ttk.Treeview(self.frame, column=self.columns, show="headings",
                                 selectmode="browse", height=10)

        self.tree.heading("#1", text="Date")
        self.tree.heading("#2", text="Time")
        self.tree.column("#1", width=197, anchor="center")
        self.tree.column("#2", width=147, anchor="center")
        self.tree.pack()

        # Add double click select function
        self.tree.bind('<<TreeviewSelect>>', self.create_buttons)

        # Actions canvas
        self.actions_frame = tk.Frame(self.frame, height=60, width=200)
        self.actions_frame.pack()
        self.actions_frame.configure(height=self.actions_frame["height"], width=self.actions_frame["width"])
        self.actions_frame.pack_propagate(False)

        # Action buttons frame
        self.r_buttons_frame = tk.Frame(self.actions_frame)
        self.r_buttons_frame.pack()

        # Select appointment instructions
        self.instructions_label = tk.Label(self.actions_frame, text='Select an availability slot')
        self.instructions_label.pack()

        self.show_appointments()

        self.frame.pack(padx=10, pady=20)

    def create_times(self, values, variable):
        """
        @param values: List containing the day of the week (0-5) and times
        @param variable: variable of the weekday
        @return: returns modified self.availability_days_times dictionary
        """

        if (variable.get()) != 0:
            if values[0] in self.availability_days_times:
                self.availability_days_times[values[0]].append([values[1][0], values[1][1]])
            else:
                self.availability_days_times[values[0]] = [[values[1][0], values[1][1]]]
        else:
            self.availability_days_times.pop(values[0])

    def confirm(self):
        """
        actions the confirm button
        """
        # Gets the dates from the date entry
        self.start_end["start"] = self.start_date.get()
        self.start_end["end"] = self.end_date.get()

        # Sets limitations of date entry
        if self.start_end["start"] > self.start_end["end"]:
            return messagebox.showinfo("Date entry error",
                                       "Start date cannot come after end date")
        elif self.start_end["start"] < date.today().strftime('%Y-%m-%d'):
            return messagebox.showinfo("Date entry error",
                                       "Start date cannot come before today's date")

        # Generate date_list and availability day times
        dates_list = self.count_dates(self.start_end)
        availability_days = self.create_availability_list(dates_list, self.availability_days_times)

        # Insert availability slots into db and refresh slot table on page
        self.insert_slots(availability_days, self.doctor_id)
        self.show_appointments()

    def create_availability_list(self, dates_list, availability_days_times):
        """

        @param dates_list: dates in every affected week
        @param availability_days_times: available times in a weekday
        @return: returns every availability day with working hours
        """
        availability_days = []
        start_date = datetime.datetime.strptime(self.start_end["start"], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(self.start_end["end"], "%Y-%m-%d").date()
        for i in dates_list:
            now = i

            for weekday in availability_days_times.keys():
                for time_range in availability_days_times[weekday]:
                    list_date = now - datetime.timedelta(days=now.weekday()) + datetime.timedelta(days=weekday)
                    start_time = str(str(list_date) + " " + time_range[0])
                    end_time = str(str(list_date) + " " + time_range[1])

                    if (start_date <= list_date <= end_date) and ([start_time, end_time] not in availability_days):
                        availability_days.append([start_time, end_time])

        return availability_days

    @staticmethod
    def count_dates(start_end):
        """

        @param start_end: start date of the period, end date of the period
        @return: counts date in every affected week
        """
        try:
            start_date = datetime.datetime.strptime(start_end["start"], "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(start_end["end"], "%Y-%m-%d").date()
        except ValueError:
            messagebox.showinfo("Please enter valid date range")
        week_delta = datetime.timedelta(days=7)
        dates_list = []
        while start_date < end_date:
            dates_list.append(start_date)
            start_date += week_delta
        dates_list.append(end_date)
        return dates_list

    def show_appointments(self):
        """
        :return: Tree view list of available appointments
        """
        # Attempts to delete existing labels and buttons
        try:
            self.instructions_label.destroy()
            self.r_buttons_frame.destroy()
        except:
            print("Refresh widget exception")

        # Deletes current slots in tree
        self.tree.delete(*self.tree.get_children())

        records = self.db.fetch_all_slots(self.doctor_id)

        # Removes slots from before today's date from db
        for time in records:
            if time[1] < date.today().strftime('%Y-%m-%d'):
                self.db.delete_slots(time[1], self.doctor_id)

        # Generates the tree
        for record in records:
            self.tree.insert("", tk.END, record[0], values=record[1:])

        if records == []:
            self.instructions_label = tk.Label(self.actions_frame, text='You have no booked availability')
        else:
            self.instructions_label = tk.Label(self.actions_frame, text='Select an availability slot')

        self.instructions_label.pack()

    @staticmethod
    def create_slots(availability_days):
        """
        :param availability_days: List of days and times of shifts
        :return: Generation of slots between available dates
        """
        slots = []
        for i in availability_days:
            counter = datetime.datetime.strptime(i[0], '%Y-%m-%d %H:%M:%S')
            endtime = datetime.datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S')
            stopper = 0
            while counter != endtime and stopper < 100:
                if counter not in slots:
                    slots.append(counter)
                counter += datetime.timedelta(minutes=20)

                stopper += 1

        return slots

    def insert_slots(self, availability_days, doctor_id):
        """
        :param availability_days: days of availability
        :param doctor_id: Session ID
        :return: inserts available slots into db
        """
        conn = sqlite3.connect("database.db")
        slots = self.create_slots(availability_days)
        counter_error = 0
        counter_success = 0
        c = conn.cursor()
        for i in slots:
            start_time = i.strftime("%Y-%m-%d %H:%M:%S")
            selectstatement = "SELECT * FROM Slots WHERE doctorID='{0}' and startTime='{1}'".format(
                doctor_id, start_time)
            c.execute(selectstatement)
            results = c.fetchall()
            print(results)
            if len(results) < 1:
                try:
                    statement = "INSERT into Slots('doctorID', 'startTime') VALUES ( '{0}' , '{1}')".format(
                        doctor_id, start_time)
                except:
                    pass
                print(statement)
                c.execute(statement)
                conn.commit()
                counter_success += 1
            else:
                print("Record Exist")
                counter_error += 1
        if len(slots) >= 1:
            if counter_error == 0:
                messagebox.showinfo("Success", 'All records were inserted')
            elif counter_success == 0:
                messagebox.showinfo("Duplicate error", 'All slots are in the database already')
            elif counter_error >= 1:
                messagebox.showinfo("Some records were not inserted",
                                    str(counter_error) + " records already exist in the database")
        else:
            messagebox.showinfo("No viable days", "No chosen weekdays between the date range")

        conn.close()


# allows page to be opened directly from .py file with placeholder userID
if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.wm_title('Djekiin Health: GP')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.resizable(False, False)
        gl.main_window = root
        doctor_id = 10
        GpAvailability(root, doctor_id)
        root.mainloop()


    main()
