import tkinter as tk
from tkinter import ttk

from languages import *


class SettingsWindow(tk.Frame):
    """
        This is, without a doubt, some of the worst code I have ever written.
        To anyone looking through this, I am very sorry.
        I will probably come back and clean this up some day.
        But we all know how that goes...

        This is never going to get touched again...
    """

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw', expand=True, fill='both')

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text=languages[self.parent.save_m.data['language']]['settings']['settings_heading'],
                  font=self.parent.heading_font).pack(side='left')

        theme_frame = ttk.Frame(main_frame)
        theme_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(theme_frame,
                  text=languages[self.parent.save_m.data['language']]['settings']['settings_theme']).pack(side='left')
        self.theme_var = tk.StringVar(theme_frame)
        self.theme_var.set(self.parent.save_m.data['theme'].capitalize())
        theme_dropdown = ttk.OptionMenu(theme_frame, self.theme_var, *['Dark', 'Light', 'System'])
        theme_dropdown.pack(side='left')
        theme_dropdown.configure(state=self.parent.save_m.settings_enabled)

        update_frame = ttk.Frame(main_frame)
        update_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.update_var = tk.StringVar(update_frame)
        self.update_var.set(self.parent.save_m.data['automatic_update_check'])
        ttk.Checkbutton(update_frame,
                        text=languages[self.parent.save_m.data['language']]['settings']['settings_update_check'],
                        variable=self.update_var,
                        onvalue='allowed',
                        offvalue='disallowed').pack(side='left')

        checkout_frame = ttk.Frame(main_frame)
        checkout_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.checkout_var = tk.StringVar(checkout_frame)
        self.checkout_var.set(self.parent.save_m.data['show_checkout_menu'])
        ttk.Checkbutton(checkout_frame,
                        text=languages[self.parent.save_m.data['language']]['settings']['settings_show_checkout'],
                        variable=self.checkout_var,
                        onvalue='allowed',
                        offvalue='disallowed').pack(side='left')

        developer_frame = ttk.Frame(main_frame)
        developer_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.developer_var = tk.StringVar(developer_frame)
        self.developer_var.set(self.parent.save_m.data['show_developer_menu'])
        ttk.Checkbutton(developer_frame,
                        text=languages[self.parent.save_m.data['language']]['settings']['settings_show_developer'],
                        variable=self.developer_var,
                        onvalue='allowed',
                        offvalue='disallowed').pack(side='left')

        help_frame = ttk.Frame(main_frame)
        help_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.help_var = tk.StringVar(help_frame)
        self.help_var.set(self.parent.save_m.data['show_help_menu'])
        ttk.Checkbutton(help_frame,
                        text=languages[self.parent.save_m.data['language']]['settings']['settings_show_help'],
                        variable=self.help_var,
                        onvalue='allowed',
                        offvalue='disallowed').pack(side='left')

        users_frame = ttk.Frame(main_frame)
        users_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.users_var = tk.StringVar(users_frame)
        self.users_var.set(self.parent.save_m.data['show_users_menu'])
        ttk.Checkbutton(users_frame,
                        text=languages[self.parent.save_m.data['language']]['settings']['settings_show_users'],
                        variable=self.users_var,
                        onvalue='allowed',
                        offvalue='disallowed').pack(side='left')

        save_settings_frame = ttk.Frame(main_frame)
        save_settings_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Button(save_settings_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompts_save_changes'],
                   command=lambda: self.prepare_for_save()).pack()

        ttk.Label(main_frame, text=f'Settings Version: {self.parent.save_m.data["settings_version"]}').pack()

    def prepare_for_save(self):
        """
            converts the information from the settings fields to being something that is
            usable for the program
            :return:
        """

        self.parent.save_m.data['automatic_update_check'] = self.update_var.get()
        self.parent.save_m.data['theme'] = self.theme_var.get()
        self.parent.save_m.data['show_checkout_menu'] = self.checkout_var.get()
        self.parent.save_m.data['show_developer_menu'] = self.developer_var.get()
        self.parent.save_m.data['show_help_menu'] = self.help_var.get()
        self.parent.save_m.data['show_users_menu'] = self.users_var.get()

        self.parent.save_m.push_save()
        self.parent.menu_bar.generate()

        self.parent.tab_controller.select(0)
        self.destroy()
