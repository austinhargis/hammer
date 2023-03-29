import tkinter as tk


class SettingsWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.title('Settings')

        theme_frame = tk.Frame(self)
        theme_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2,
                         pady=(self.parent.padding * 2, self.parent.padding))
        tk.Label(theme_frame, text='Theme').pack(side='left')
        self.theme_var = tk.StringVar(theme_frame)
        self.theme_var.set(self.parent.save_m.data['theme'].capitalize())
        theme_dropdown = tk.OptionMenu(theme_frame, self.theme_var, *['Dark', 'Light', 'System'])
        theme_dropdown.pack(side='right')
        theme_dropdown.configure(state=self.parent.save_m.settings_enabled)

        update_frame = tk.Frame(self)
        update_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        tk.Label(update_frame, text='Automatic Update').pack(side='left')
        self.update_var = tk.StringVar(update_frame)
        self.update_var.set(self.parent.save_m.data['automatic_updates'].capitalize())
        update_dropdown = tk.OptionMenu(update_frame, self.update_var, *['Enabled', 'Disabled'])
        update_dropdown.pack(side='right')
        update_dropdown.configure(state='disabled')

        developer_frame = tk.Frame(self)
        developer_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        tk.Label(developer_frame, text='Show Developer Menu').pack(side='left')
        self.developer_var = tk.StringVar(developer_frame)
        self.developer_var.set(self.parent.save_m.data['show_developer_menu'].capitalize())
        developer_dropdown = tk.OptionMenu(developer_frame, self.developer_var, *['Enabled', 'Disabled'])
        developer_dropdown.pack(side='right')
        developer_dropdown.configure(state=self.parent.save_m.settings_enabled)

        save_settings_frame = tk.Frame(self)
        save_settings_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=(self.parent.padding,
                                                                                               self.parent.padding * 2))
        tk.Button(save_settings_frame, text='Save Settings', command=lambda: self.prepare_for_save()).pack()

        tk.Label(self, text=f'Settings Version: {self.parent.save_m.data["settings_version"]}').pack()

        self.mainloop()

    def prepare_for_save(self):
        """
            converts the information from the settings fields to being something that is
            usable for the program
            :return:
        """

        self.parent.save_m.data['automatic_updates'] = self.update_var.get().lower()
        self.parent.save_m.data['theme'] = self.theme_var.get().lower()
        self.parent.save_m.data['show_developer_menu'] = self.developer_var.get().lower()

        self.parent.save_m.push_save()
        self.parent.menu_bar.generate()

        self.destroy()
