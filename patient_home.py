import tkinter as tk
import navbar
import gl
import webbrowser


class PatientHome(navbar.NavBarPatient):

    def __init__(self, master, patient_id):
        """Set GUI widgets"""

        super().__init__(master)
        PatientHome.patient_id = patient_id

        # master frame
        self.master = master

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # COVID alert banner

        self.warning = tk.Label(self.frame, text="ALERT: LONDON IS AT COVID TIER LEVEL 4", fg="yellow", bg="#ff0f0f",
                                font="TkTextFont 14", width=54)
        self.warning.pack()

        # Welcome text
        self.welcome = tk.LabelFrame(self.frame, text='Home')
        self.welcome.pack(padx=10, pady=(0, 10))

        self.label = tk.Label(self.welcome, text='Welcome to the Homepage of your GP health portal!', width=80)
        self.label.grid(row=0)
        self.label2 = tk.Label(self.welcome,
                               text='You can navigate the portal by clicking on the menu in the top left. ', width=80)
        self.label2.grid(row=1)

        # Coronavirus advice
        self.link1 = tk.Label(self.welcome,
                              text="Click here for the latest NHS information and advice about coronavirus.", fg="blue",
                              cursor="hand2")
        self.link1.grid(row=2)
        self.link1.bind("<Button-1>",
                        lambda e: webbrowser.open_new("https://www.nhs.uk/conditions/coronavirus-covid-19/"))

        self.label3 = tk.Label(self.welcome, text=' ', width=80, height=40)
        self.label3.grid(row=3)


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.resizable(False, False)
        root.wm_title('Djekiin Health: Patient')
        root.wm_iconbitmap('images/djekiin_logo.ico')

        root.config(bg="white")
        gl.main_file = root

        PatientHome(root, 1)

        root.mainloop()


    main()
