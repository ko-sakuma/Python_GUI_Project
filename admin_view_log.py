import tkinter as tk
from tkinter import ttk
import navbar
import gl


class ViewLog(navbar.NavBarAdmin):
    def __init__(self, master):
        # Call up the menu bar items:
        super().__init__(master)

        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True)

        # Create a description
        self.description = tk.Label(self.frame,
                                    text="A record of which member of staff viewed whose patient record at what time")
        self.description.pack(padx=150, pady=10, expand="true")

        # Create a frame to insert log information
        self.text_frame = tk.LabelFrame(self.frame, text="Viewers Log", width=100, height=600)
        self.text_frame.pack(padx=10, pady=10, fill="both")

        # create a treeview to display information:
        the_tree = ttk.Treeview(self.text_frame, height=27, column="full_info", show="tree", selectmode="none")
        the_tree.column("full_info", width=800, anchor="w")
        the_tree.pack(padx=10, pady=10, fill="both")
        the_tree.column("#0", width=0, minwidth=10)

        # Open log file in read-only mode and insert into frame
        with open('ViewersLog.txt', "r") as f:
            hard_log = (line.split("\n") for line in f)
            for x in hard_log:
                the_tree.insert("", tk.END, values=x)


if __name__ == '__main__':
    def main():
        root = tk.Tk()
        # root.resizable(False, False)
        root.title('Djekiin Health')
        gl.main_window = root
        ViewLog(root)
        root.mainloop()


    main()
