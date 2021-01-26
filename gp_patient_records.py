# GP's patient search function is the same as admin's function

from admin_patient_records import *


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        root.wm_title('Djekiin Health: GP')
        root.wm_iconbitmap('images/djekiin_logo.ico')
        root.resizable(False, False)

        AdminPatientSearch(root, "gp", 1)  # Calls up patient search page as a GP
        root.mainloop()


    main()
