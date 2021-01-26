import tkinter as tk
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

    def fetch_gp_info_from_column(self, gp_id, column):
        self.c.execute(f"SELECT {column} FROM Staff WHERE userID = {gp_id}")
        records = self.c.fetchone()
        var = records[0]
        return var


class GpProfile(navbar.NavBarGP):
    def __init__(self, master, gp_id):
        # Call up the menu bar items:
        super().__init__(master)

        self.gp_id = gp_id
        self.db = SqliteQueries("database.db")
        self.master = master
        self.frame = tk.Frame(self.master)

        self.labelframe = tk.LabelFrame(self.frame, text="My Profile")
        self.labelframe.grid(column=0, row=7, padx=20, pady=60)

        # Create frames for the input fields

        # First Name
        entry_text_first_name = tk.StringVar()
        self.f_name = tk.Entry(self.labelframe, textvariable=entry_text_first_name, width=30)
        entry_text_first_name.set(self.db.fetch_gp_info_from_column(self.gp_id, "firstName"))
        self.f_name.grid(row=0, column=1, padx=20)
        self.f_name_label = tk.Label(self.labelframe, text='First Name')
        self.f_name_label.grid(row=0, column=0)

        # Last Name
        entry_text_last_name = tk.StringVar()
        self.l_name = tk.Entry(self.labelframe, textvariable=entry_text_last_name, width=30)
        entry_text_last_name.set(self.db.fetch_gp_info_from_column(self.gp_id, "lastName"))
        self.l_name.grid(row=1, column=1, padx=20)
        self.l_name_label = tk.Label(self.labelframe, text='Last Name')
        self.l_name_label.grid(row=1, column=0)

        # Full Address
        entry_text_address = tk.StringVar()
        self.address = tk.Entry(self.labelframe, textvariable=entry_text_address, width=30)
        entry_text_address.set(self.db.fetch_gp_info_from_column(self.gp_id, "address"))
        self.address.grid(row=2, column=1, padx=20)
        self.address_label = tk.Label(self.labelframe, text='Full Address')
        self.address_label.grid(row=2, column=0)

        # Email
        entry_text_email = tk.StringVar()
        self.email = tk.Entry(self.labelframe, textvariable=entry_text_email, width=30)
        entry_text_email.set(self.db.fetch_gp_info_from_column(self.gp_id, "email"))
        self.email.grid(row=3, column=1, padx=20)
        self.email_label = tk.Label(self.labelframe, text='Email')
        self.email_label.grid(row=3, column=0)

        # Phone
        entry_text_phone_number = tk.StringVar()
        self.phone = tk.Entry(self.labelframe, textvariable=entry_text_phone_number, width=30)
        entry_text_phone_number.set(self.db.fetch_gp_info_from_column(self.gp_id, "phoneNumber"))
        self.phone.grid(row=4, column=1, padx=20)
        self.phone_label = tk.Label(self.labelframe, text='Phone')
        self.phone_label.grid(row=4, column=0)

        # Create a submit button
        self.submit_btn = tk.Button(self.labelframe, text='Save Changes', command=self.submit)
        self.submit_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        self.frame.pack()

    def submit(self):
        con = sqlite3.connect("database.db")
        c = con.cursor()
        query = '''UPDATE Staff SET address = ?, firstName= ?, lastName= ?, phoneNumber= ?, email= ? WHERE userID = ? 
        '''
        values = (
            self.address.get(), self.f_name.get(), self.l_name.get(), self.phone.get(), self.email.get(), self.gp_id)
        c.execute(query, values)
        con.commit()
        messagebox.showinfo("Success", 'Changes made successfully')
        con.close()


if __name__ == '__main__':
    def main():
        import gl
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health: GP')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        gl.main_window = root
        GpProfile(root, 2)

        root.mainloop()


    main()

# #sqlite class:
