import tkinter as tk


# the cascading menu:
class menu_bar:
    def __init__(self, master):
        """create menu item"""

        # define a menu item:
        self.my_menu = tk.Menu(master)

        # let the master know to use the menu item:
        master.config(menu=self.my_menu)

        # create a new menu item:
        self.file_menu = tk.Menu(self.my_menu)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Logout", command=self.logout)
        self.file_menu.add_command(label="Exit", command=master.destroy)

    def logout(self):
        import gl
        import login
        gl.main_window.destroy()
        gl.main_window.quit()
        # pass
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.config(bg="white")
        gl.main_file = root
        login.Login(root)
        root.mainloop()
        pass


# the parent class of NavBar:
class NavBarAbs(menu_bar):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.color = {"nero": "#252726", "white": "#FFFFFF",
                      "NHS_Blue": "#005EB8", "NHS_DarkBlue": "#003087", "NHS_BrighBlue": "#0072CE",
                      "NHS_LightBlue": "#41B6E6", "NHS_AquaBlue": "#00A9CE",
                      "NHS_Black": "#231f20", "NHS_DarkGrey": "#425563", "NHS_MidGray": "#768692",
                      "NHS_PaleGrey": "#E8EDEE"}

        self.topFrame = tk.Frame(self.master, bg=self.color["NHS_Blue"])
        self.topFrame.pack(side='top', fill=tk.X)

        self.nhs_logo = tk.PhotoImage(file=r"images/NHS_logo.png")
        self.homeLabel = tk.Label(self.topFrame, image=self.nhs_logo)

        self.homeLabel.pack(side='right', padx=(0,10))

        self.btnState = False

        self.navIcon = tk.PhotoImage(file="images/menu.png")

        self.closeIcon = tk.PhotoImage(file="images/close.png")
        self.navBarBtn = tk.Button(self.topFrame, image=self.navIcon, bg=self.color["NHS_Blue"],
                                   activebackground=self.color["NHS_Blue"], bd=0, command=self.switch)

        self.navBarBtn.pack(side='left', padx=10)

        self.navRoot = tk.Frame(self.master, bg=self.color["NHS_PaleGrey"], height=1000, width=200)
        self.navRoot.place(x=-300, y=0)
        self.navLabel = tk.Label(self.navRoot, font=('', 15), bg=self.color["NHS_DarkBlue"], fg="black", height=2,
                                 width=300, padx=20).place(x=0, y=0)

        self.closeBtn = tk.Button(self.navRoot, image=self.closeIcon, bg=self.color["NHS_Blue"],
                                  activebackground=self.color["NHS_Blue"], bd=0, command=self.switch)
        self.closeBtn.place(x=150, y=5)

    def switch(self):
        global btnState
        if self.btnState is True:
            # create animated Navbar closing:

            self.navRoot.place(x=-300, y=0)  # hiding the Nav Bar behind the frame
            self.topFrame.update()

            # resetting widget self.colors:
            # brandLabel.config(bg="white", fg=self.color["NHS_Blue"])
            self.homeLabel.config(bg=self.color["NHS_Blue"])
            self.topFrame.config(bg=self.color["NHS_Blue"])
            # self.frame.config(bg= self.color['nero'])

            # turning button OFF:
            self.btnState = False
        else:
            self.homeLabel.config(bg=self.color["NHS_Blue"])
            self.topFrame.config(bg=self.color["NHS_Blue"])

            # created animated Navbar opening:
            self.navRoot.lift()

            self.navRoot.place(x=0, y=0)
            self.topFrame.update()

            # turing button ON:
            self.btnState = True

    def buttons(self, button_text, button_command, button_placement):

        y_location = (button_placement * 40) + 40

        tk.Button(self.navRoot, text=button_text, font=('', 10),
                  bg=self.color["white"],
                  fg=self.color["NHS_Blue"],
                  activebackground=self.color["NHS_Blue"],
                  activeforeground=self.color["NHS_PaleGrey"],
                  bd=2, command=button_command, relief='groove',
                  width=17).place(x=25, y=y_location)

    def destroy_frames(self):
        self.topFrame.destroy()
        self.navRoot.destroy()
        self.frame.destroy()


# the navbar for admin:
class NavBarAdmin(NavBarAbs):
    def __init__(self, master):

        super().__init__(master)

        # creating the buttons usign the buttons method we made:
        self.buttons("Home", self.homePage, 1)
        self.buttons("My Profile", self.profilePage, 2)
        self.buttons("Register GPs", self.registerGPs, 3)
        self.buttons("Register Patients", self.registerPatients, 4)
        self.buttons("Staff Profiles", self.staffProfiles, 5)
        self.buttons("Patients", self.patientsPage, 6)
        self.buttons("Viewers Log",self.logPage,7)

    def homePage(self):
        import admin_home

        self.destroy_frames()

        try:
            admin_home.AdminHome(self.master, admin_home.AdminHome.staff_id)
        except AttributeError:
            admin_home.AdminHome(self.master, 1)

    def profilePage(self):
        import admin_my_profile
        import admin_home

        self.destroy_frames()

        try:
            admin_my_profile.AdminProfile(self.master, admin_home.AdminHome.staff_id)
        except AttributeError:
            admin_my_profile.AdminProfile(self.master, 2)
            print("We've just placed dummy data. Please log in for real world scenario")

    def registerGPs(self):
        import admin_register_gps

        self.destroy_frames()

        admin_register_gps.AdminRegisterGP(self.master)

    def registerPatients(self):

        import admin_register_patients

        self.destroy_frames()

        admin_register_patients.admin_confirmation_patients(self.master)

    def staffProfiles(self):
        import admin_staff_profile

        self.destroy_frames()

        admin_staff_profile.AdminStaffSearch(self.master)

    def patientsPage(self):
        import admin_patient_records
        import admin_home

        self.destroy_frames()

        try:
            admin_patient_records.AdminPatientSearch(self.master, 'admin', admin_home.AdminHome.staff_id)
        except AttributeError:
            admin_patient_records.AdminPatientSearch(self.master, 'admin', 2)

    def logPage(self):
        import admin_view_log

        self.destroy_frames()

        admin_view_log.ViewLog(self.master)


# the navbar for GP:
class NavBarGP(NavBarAbs):
    def __init__(self, master):

        super().__init__(master)

        self.buttons("Home", self.homePage, 1)
        self.buttons("My Profile", self.myProfile, 2)
        self.buttons("Patient Records", self.patientRecords, 3)
        self.buttons("Appointments", self.appointments, 4)
        self.buttons("Set Availability", self.availability, 5)

    def homePage(self):
        import gp_home

        self.destroy_frames()

        try:
            gp_home.GPHome(self.master, gp_home.GPHome.staff_id)
        except AttributeError:
            gp_home.GPHome(self.master, 1)

    def myProfile(self):
        import gp_home
        import gp_my_profile
        self.destroy_frames()

        try:
            gp_my_profile.GpProfile(self.master, gp_home.GPHome.staff_id)
        except AttributeError:
            gp_my_profile.GpProfile(self.master, 1)
        pass

    def patientRecords(self):
        import gp_patient_records
        import gp_home
        self.destroy_frames()
        try:
            gp_patient_records.AdminPatientSearch(self.master, 'gp', gp_home.GPHome.staff_id)
        except AttributeError:
            gp_patient_records.AdminPatientSearch(self.master, 'gp', 1)

    def appointments(self):
        import gp_appointments
        import gp_home
        self.destroy_frames()

        try:
            gp_appointments.GpAppointment(self.master, gp_home.GPHome.staff_id)
        except AttributeError:
            gp_appointments.GpAppointment(self.master, 1)

    def availability(self):
        import gp_set_availability
        import gp_home
        self.destroy_frames()
        try:
            gp_set_availability.GpAvailability(self.master,gp_home.GPHome.staff_id)
        except AttributeError:
            gp_set_availability.GpAvailability(self.master,2)


class NavBarPatient(NavBarAbs):
    def __init__(self, master):

        super().__init__(master)

        self.buttons("Home", self.homePage, 1)
        self.buttons("My Profile", self.myProfile, 2)
        self.buttons("View Appointments", self.viewAppointments, 3)
        self.buttons("Book Appointments", self.bookAppointments, 4)
        self.buttons("My Medical Records", self.myRecord, 5)

    def homePage(self):
        import patient_home
        self.destroy_frames()
        try:
            patient_home.PatientHome(self.master, patient_home.PatientHome.patient_id)
        except AttributeError:
            patient_home.PatientHome(self.master, 1)

    def myProfile(self):
        import patient_home
        import patient_my_profile
        self.destroy_frames()
        try:
            patient_my_profile.PatientProfile(self.master, patient_home.PatientHome.patient_id)
        except AttributeError:
            patient_my_profile.PatientProfile(self.master, 1)

    def viewAppointments(self):
        import patient_home
        import patient_appointments
        self.destroy_frames()
        try:
            patient_appointments.PatientAppointments(self.master, patient_home.PatientHome.patient_id)
        except AttributeError:
            patient_appointments.PatientAppointments(self.master, 1)

    def bookAppointments(self):
        import patient_home
        import patient_book_appointment
        self.destroy_frames()
        try:
            patient_book_appointment.PatientAppointments(self.master, patient_home.PatientHome.patient_id)
        except AttributeError:
            patient_book_appointment.PatientAppointments(self.master, 1)
            print("Dummy data. Please log in to schedule for specific person")

    def myRecord(self):
        import patient_home
        import patient_my_record
        self.destroy_frames()
        try:
            patient_my_record.PatientRecord(self.master, patient_home.PatientHome.patient_id, "patient")
        except AttributeError:
            patient_my_record.PatientRecord(self.master, 2, "patient")


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.title("Menu")
        root.config(bg="white")

        NavBarAdmin(root)

        root.mainloop()


    main()
