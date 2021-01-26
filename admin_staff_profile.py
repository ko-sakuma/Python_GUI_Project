import tkinter as tk
from tkinter import ttk
import sqlite3
import navbar
import gl


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
        :param table_entered: table (and column names if required) in db
        :param columns: columns to update
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


class AdminStaffSearch(navbar.NavBarAdmin):
    """A class to create GUI interface for admin staff profile"""

    def __init__(self, master):
        """
        Constructs all the necessary attributes for the AdminPatientSearch object.
        :param master: TKinter master
        """

        # call up the menu bar items:
        super().__init__(master)

        self.master = master
        self.frame = tk.Frame(self.master)
        self.btn_click = ""

        # create main label frame
        self.admin_patient_frame = tk.LabelFrame(self.frame, text='Staff Profiles')
        self.admin_patient_frame.grid(row=0, pady=10, padx=10)

        # create search frame
        self.search_frame = tk.LabelFrame(self.admin_patient_frame, text='Search Staff')
        self.search_frame.grid(row=0, pady=10, padx=10)
        self.search_frame.columnconfigure([0, 1], minsize=360)

        # create entries
        self.position = tk.Entry(self.search_frame, width=40)
        self.position.grid(row=0, column=1, padx=20)

        self.f_name = tk.Entry(self.search_frame, width=40)
        self.f_name.grid(row=1, column=1, padx=20)

        self.l_name = tk.Entry(self.search_frame, width=40)
        self.l_name.grid(row=2, column=1, padx=20)

        self.email = tk.Entry(self.search_frame, width=40)
        self.email.grid(row=5, column=1, padx=20)

        self.phone = tk.Entry(self.search_frame, width=40)
        self.phone.grid(row=6, column=1, padx=20)

        # create text box labels
        self.position_label = tk.Label(self.search_frame, text='Position')
        self.position_label.grid(row=0, column=0)

        self.f_name_label = tk.Label(self.search_frame, text='First Name')
        self.f_name_label.grid(row=1, column=0)

        self.l_name_label = tk.Label(self.search_frame, text='Last Name')
        self.l_name_label.grid(row=2, column=0)

        self.email_label = tk.Label(self.search_frame, text='Email')
        self.email_label.grid(row=5, column=0)

        self.phone_label = tk.Label(self.search_frame, text='Phone')
        self.phone_label.grid(row=6, column=0)

        # create query button
        self.query_all_btn = tk.Button(self.search_frame, text='Show all staff',
                                       width=28, command=self.show_all_record)
        self.query_all_btn.grid(row=8, column=0, columnspan=1, pady=10, padx=10)

        self.query_btn = tk.Button(self.search_frame, text='Search staff', width=28,
                                   command=self.search_record)
        self.query_btn.grid(row=8, column=1, columnspan=1, pady=10, padx=10)

        # create result frame
        self.result_frame = tk.LabelFrame(self.admin_patient_frame, text='Result')
        self.result_frame.grid(row=1, pady=10, padx=10)
        self.result_frame.columnconfigure([0], minsize=720)

        # create instructions
        self.result_label = tk.Label(self.result_frame,
                                     text='Double click record to bring up details or remove the account. ')
        self.result_label.grid(row=0, column=0, pady=2, padx=10, sticky='w')

        # create treeview columns
        self.columns = ["firstName", "lastName", "role", "email", "phoneNumber", "active"]
        self.tree = ttk.Treeview(self.result_frame, column=self.columns, show="headings",
                                 selectmode="browse", height=7)
        for c in self.columns:
            self.tree.column(c, width=90)
        self.asp_scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.tree.yview)
        self.asp_scrollbar.grid(row=1, column=0, padx=(0, 15), pady=(10, 15), sticky="nes")
        self.tree.configure(yscrollcommand=self.asp_scrollbar.set)

        self.tree.column("#1", width=90)
        self.tree.column("#2", width=90)
        self.tree.column("#3", width=70)
        self.tree.column("#4", width=90)
        self.tree.column("#5", width=90)
        self.tree.column("#6", width=20)
        self.tree.heading("#1", text="First Name")
        self.tree.heading("#2", text="Last Name")
        self.tree.heading("#3", text="Position")
        self.tree.heading("#4", text='Email')
        self.tree.heading("#5", text='Phone')
        self.tree.heading("#6", text='Active')
        self.tree.grid(row=1, column=0, pady=10, padx=10, ipadx=100)

        # Add double click select function
        self.tree.bind("<Double-1>", self.double_click)

        self.frame.pack()

    def search_record(self):
        """
        Searches staff record
        :return: staff records matching the criteria
        """

        # set button click indicator
        self.btn_click = "search_record"

        # deletes current rows in tree:
        self.tree.delete(*self.tree.get_children())

        # create class instance for the database:
        db = SqliteQueries('database.db')

        # active records
        records = db.execute("SELECT firstName, lastName, role, \
                                  email, phoneNumber, userID \
                              FROM Staff\
                              WHERE firstName LIKE ?\
                                  AND lastName LIKE ?\
                                  AND role LIKE ?\
                                  AND email LIKE ?\
                                  AND replace(replace(replace(replace(replace(replace(\
                                      phoneNumber,'+',''),'-',''),' ',''),'(',''),')','')\
                                      ,'.','') LIKE ?",
                             ('%' + self.f_name.get() + '%',
                              '%' + self.l_name.get() + '%',
                              '%' + self.position.get() + '%',
                              '%' + self.email.get() + '%',
                              '%' + self.phone.get() + '%'))
        for record in records:
            self.tree.insert("", tk.END, record[5], values=record[0:5])
            try:
                self.tree.set(record[5], "5", "Yes")
            except:
                pass

        # deactivated records
        records = db.execute("SELECT firstName, lastName, role, \
                                          email, phoneNumber, userID \
                                      FROM DeactiveStaff\
                                      WHERE firstName LIKE ?\
                                          AND lastName LIKE ?\
                                          AND role LIKE ?\
                                          AND email LIKE ?\
                                          AND replace(replace(replace(replace(replace(replace(\
                                              phoneNumber,'+',''),'-',''),' ',''),'(',''),')','')\
                                              ,'.','') LIKE ?",
                             ('%' + self.f_name.get() + '%',
                              '%' + self.l_name.get() + '%',
                              '%' + self.position.get() + '%',
                              '%' + self.email.get() + '%',
                              '%' + self.phone.get() + '%'))
        for record in records:
            self.tree.insert("", tk.END, record[5], values=record[0:5])
            try:
                self.tree.set(record[5], "5", "No")
            except:
                pass

    def show_all_record(self):
        """
        Shows all records in the database
        :return: all records in the database
        """

        # set button click indicator
        self.btn_click = "show_all_record"

        # deletes current rows in tree:
        self.tree.delete(*self.tree.get_children())

        # create class instance for the database:
        db = SqliteQueries('database.db')

        # fetch records from SqliteQueries:
        records = db.execute("SELECT firstName, lastName, role, \
                                  email, phoneNumber, userID \
                              FROM Staff")
        for record in records:
            self.tree.insert("", tk.END, record[5], values=record[0:5])
            self.tree.set(record[5], "5", "Yes")

        records = db.execute("SELECT firstName, lastName, role, \
                                         email, phoneNumber, userID \
                                     FROM DeactiveStaff")
        for record in records:
            self.tree.insert("", tk.END, record[5], values=record[0:5])
            self.tree.set(record[5], "5", "No")

    def double_click(self, event):
        """
        Makes two buttons appear once the user double clicks on a patient
        :param event: double click event
        :return: "show details" and "Delete record button"
        """

        row_id = self.tree.identify_row(event.y)

        # clear existing button
        try:
            self.show_details.grid_forget()
            self.delete.grid_forget()
            self.deactivate.grid_forget()
            self.active.grid_forget()
        except:
            print("No button generated")

        self.show_details = tk.Button(self.result_frame, width=15, text="Show details",
                                      command=lambda tree=self.tree,
                                      table='Staff': self.create_popup(event, tree, table))
        if self.tree.item(item=row_id)['values'][5] == "No":
            self.active = tk.Button(self.result_frame, width=15, text="Activate",
                                    command=lambda: self.activate_staff(row_id))
            self.active.grid(row=2, column=0, pady=10, padx=(10, 130), sticky='e')
        else:
            self.deactivate = tk.Button(self.result_frame, width=15, text="Deactivate",
                                        command=lambda: self.deactivate_staff(row_id))
            self.deactivate.grid(row=2, column=0, pady=10, padx=(10, 130), sticky='e')

        self.delete = tk.Button(self.result_frame, width=15, text="Delete",
                                command=lambda: self.delete_staff(row_id))
        self.show_details.grid(row=2, column=0, pady=10, padx=(70, 10), sticky='w')
        self.delete.grid(row=2, column=0, pady=10, padx=(10, 10), sticky='e')

    def create_popup(self, event, tree, table):
        """
        Creates pop-up and autoloads fields based on row clicked on, you must ensure correct inputs passed in
        :param event: User click on treeview row
        :param tree: the name of tree view attribute e.g. (self.cons_frame_tree)
        :param table: name of database table that treeview is pulling data from
        :return: pop-up with editable fields filled with row data and labelled with treeview column names
        """

        # delete buttons
        self.show_details.grid_forget()
        self.delete.grid_forget()
        try:
            self.deactivate.grid_forget()
            self.active.grid_forget()
        except:
            print("No button generated yet")

        row_id = tree.identify_row(event.y)
        self.popup = tk.Tk()
        # sb = ttk.Scrollbar(self.popup)
        # sb.pack(side='right', fill='y')
        column_list = []
        text_list = []
        for x in range(len(tree.item(item=row_id)['values'][0:5])):
            column_list.append(tree.column(x, option='id'))
            column_label = tk.Label(self.popup, text=tree.heading(x)['text'])
            column_label.pack(side="top", anchor='w', padx=20, pady=(15, 0))
            info_box = tk.Text(self.popup, width=60, height=3)
            text_list.append(info_box)
            info_box.pack(side="top", padx=20, pady=(0, 10))
            info_box.insert("insert", tree.item(item=row_id)['values'][x], 'grey')
        submit_button = tk.Button(self.popup, text="Update",
                                  command=lambda: self.popup_submit(event, column_list, table, row_id, text_list))
        submit_button.pack(side="top", anchor='e', padx=20, pady=10)
        self.popup.mainloop()

    def popup_submit(self, event, columns, table, row_id, text_list):  # !!!!! new code added by Jetsun
        """
        Submits update query based on edits to popup text feilds. Create popup function creates input values,
        which means you don't need to worry about setting these
        :param event: clicking update button
        :param columns: treeview column names
        :param table: database table name
        :param row_id: id of treeview row, aligns with primary key
        :param text_list: list of textboxes in pop-up (so function knows which textbox to pull updated text from)
        :return: sends update query to
        """

        db = SqliteQueries("database.db")
        entry_values = []
        for i in range(len(text_list)):
            entry_values.append(text_list[i].get(0.0, "end"))
        db.update(table, columns, tuple(entry_values), 'userID = %s' % str(row_id))
        self.popup.destroy()

        # refresh results
        if self.btn_click == "show_all_record":
            self.show_all_record()
        elif self.btn_click == "search_record":
            self.search_record()
        else:
            pass

    def activate_staff(self, row_id):
        """
        Activates staff
        :param row_id: staff id
        :return: activate a record
        """

        # delete buttons
        self.show_details.grid_forget()
        self.delete.grid_forget()
        try:
            self.deactivate.grid_forget()
        except:
            print("No button generated")
        try:
            self.active.grid_forget()
        except:
            print("No button generated")

        # fetch record and send to active staff
        db = SqliteQueries('database.db')
        query = db.execute("SELECT * FROM DeactiveStaff WHERE userID = %d" % (int(row_id)))
        staff_record = query.fetchone()
        db.insert('Staff', staff_record)
        db.execute("DELETE FROM DeactiveStaff WHERE userID = ?",
                   (row_id,))

        # refresh results
        if self.btn_click == "show_all_record":
            self.show_all_record()
        elif self.btn_click == "search_record":
            self.search_record()

    def deactivate_staff(self, row_id):
        """
        Deactivates staff
        :param row_id: staff id
        :return: deactivate a record
        """

        # delete buttons
        self.show_details.grid_forget()
        self.delete.grid_forget()
        try:
            self.deactivate.grid_forget()
        except:
            print("No button generated")
        try:
            self.active.grid_forget()
        except:
            print("No button generated")

        # fetch record and send to deactive staff
        db = SqliteQueries('database.db')
        query = db.execute("SELECT * FROM STAFF WHERE userID = %d" % (int(row_id)))
        staff_record = query.fetchone()
        db.insert('DeactiveStaff', staff_record)
        db.execute("DELETE FROM Staff WHERE userID = ?",
                   (row_id,))

        # refresh results
        if self.btn_click == "show_all_record":
            self.show_all_record()
        elif self.btn_click == "search_record":
            self.search_record()

    def delete_staff(self, row_id):
        """
        Deletes a record
        :param row_id: staff id
        :return: delete a record
        """

        # delete buttons
        self.show_details.grid_forget()
        self.delete.grid_forget()
        try:
            self.deactivate.grid_forget()
        except:
            print("No button generated")
        try:
            self.active.grid_forget()
        except:
            print("No button generated")

        # if the user confirmed the deletion
        def delete_yes():
            self.delete_warning.destroy()
            db = SqliteQueries('database.db')
            db.execute("DELETE FROM Staff WHERE userID = ?",
                       (row_id,))

            # refresh results
            if self.btn_click == "show_all_record":
                self.show_all_record()
            elif self.btn_click == "search_record":
                self.search_record()
            else:
                pass

        # if the user did not confirm the deletion
        def delete_no():
            self.delete_warning.destroy()
            pass

        # pop up box for confirmation
        self.delete_warning = tk.Tk()
        delete_label = tk.Label(self.delete_warning, text='You are about to delete the record. Continue? ')
        delete_label.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
        delete_yes = tk.Button(self.delete_warning, text='Yes', width=15, command=delete_yes)
        delete_yes.grid(row=2, column=0, columnspan=1, pady=10, padx=10)
        delete_no = tk.Button(self.delete_warning, text='No', width=15, command=delete_no)
        delete_no.grid(row=2, column=1, columnspan=1, pady=10, padx=10)
        self.delete_warning.mainloop()


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        gl.main_window = root
        root.wm_title('Djekiin Health: Administrator')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.resizable(False, False)
        AdminStaffSearch(root)
        root.mainloop()


    main()
