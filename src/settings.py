import tkinter as tk


class SettingsWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.title('Settings')

        theme_frame = tk.Frame(self)
        theme_frame.pack(fill='both', expand=True, padx=parent.padding*2, pady=(parent.padding*2, parent.padding))
        tk.Label(theme_frame, text='Theme').pack(side='left')
        theme_var = tk.StringVar(theme_frame)
        theme_var.set('Dark')
        theme_dropdown = tk.OptionMenu(theme_frame, theme_var, *['Dark', 'Light', 'System'])
        theme_dropdown.pack(side='right')

        update_frame = tk.Frame(self)
        update_frame.pack(fill='both', expand=True, padx=parent.padding*2, pady=(parent.padding, parent.padding*2))
        tk.Label(update_frame, text='Update Checker').pack(side='left')
        update_var = tk.StringVar(update_frame)
        update_var.set('Disabled')
        update_dropdown = tk.OptionMenu(update_frame, update_var, *['Enabled', 'Disabled'])
        update_dropdown.pack(side='right')

        self.mainloop()
