import tkinter as tk


class SettingsWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.attributes('-topmost', True)
        self.title('Settings')

        tk.Label(self, text='Theme:').grid(row=0, column=0)
        theme_var = tk.StringVar(self)
        theme_var.set('Dark')
        theme_dropdown = tk.OptionMenu(self, theme_var, *['Dark', 'Light', 'System'])
        theme_dropdown.grid(row=0, column=1)

        tk.Label(self, text='Update Checker: ').grid(row=1, column=0)
        update_var = tk.StringVar(self)
        update_var.set('Disabled')
        update_dropdown = tk.OptionMenu(self, update_var, *['Enabled', 'Disabled'])
        update_dropdown.grid(row=1, column=1)

        self.mainloop()
