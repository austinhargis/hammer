import tkinter as tk


class UpdateChecker(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.attributes('-topmost', True)
        self.geometry('300x200')
        self.resizable(False, False)
        self.title('Updater')

        title_frame = tk.Frame(self)
        title_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2,
                         pady=(self.parent.padding * 2, self.parent.padding))
        tk.Label(title_frame, text='Update').pack()

        auto_update_frame = tk.Frame(self)
        auto_update_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        tk.Label(auto_update_frame, text=f'Automatic Updates {self.parent.save_m.data["automatic_updates"]}').pack()

        subtitle_frame = tk.Frame(self)
        subtitle_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        tk.Label(subtitle_frame, text=f'Last Checked {self.parent.save_m.data["last_update_check"]}').pack()

        check_update_theme = tk.Frame(self)
        check_update_theme.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=(self.parent.padding,
                                                                                              self.parent.padding * 2))
        tk.Button(check_update_theme, text='Check for Updates').pack()

        self.mainloop()
