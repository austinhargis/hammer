import tkinter as tk


class UpdateChecker(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.title('Updater')

        title_frame = tk.Frame(self)
        title_frame.pack(fill='both', expand=True, padx=parent.padding*2, pady=(parent.padding*2, parent.padding))
        tk.Label(title_frame, text='Update').pack()

        check_update_theme = tk.Frame(self)
        check_update_theme.pack(fill='both', expand=True, padx=parent.padding*2, pady=(parent.padding,
                                                                                       parent.padding*2))
        tk.Button(check_update_theme, text='Check for Updates').pack()

        self.mainloop()
