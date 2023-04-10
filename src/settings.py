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
        main_frame.pack(side='left', anchor='nw')

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
        theme_dropdown = tk.OptionMenu(theme_frame, self.theme_var, *['Dark', 'Light', 'System'])
        theme_dropdown.pack(side='right')
        theme_dropdown.configure(state=self.parent.save_m.settings_enabled)

        update_frame = ttk.Frame(main_frame)
        update_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(update_frame,
                  text=languages[self.parent.save_m.data['language']]['settings']['settings_update_check']).pack(
            side='left')
        self.update_var = tk.StringVar(update_frame)
        self.update_var.set(self.parent.save_m.data['automatic_update_check'].capitalize())
        update_dropdown = tk.OptionMenu(update_frame, self.update_var, *[
            languages[self.parent.save_m.data['language']]['settings']['setting_enabled'],
            languages[self.parent.save_m.data['language']]['settings']['setting_disabled']])
        update_dropdown.pack(side='right')
        update_dropdown.configure(state='disabled')

        checkout_frame = ttk.Frame(main_frame)
        checkout_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(checkout_frame,
                  text=languages[self.parent.save_m.data['language']]['settings']['settings_show_checkout']).pack(
            side='left')
        self.checkout_var = tk.StringVar(checkout_frame)
        self.checkout_var.set(self.parent.save_m.data['show_checkout_menu'].capitalize())
        checkout_dropdown = tk.OptionMenu(checkout_frame, self.checkout_var, *[
            languages[self.parent.save_m.data['language']]['settings']['setting_enabled'],
            languages[self.parent.save_m.data['language']]['settings']['setting_disabled']])
        checkout_dropdown.pack(side='right')
        checkout_dropdown.configure(state=self.parent.save_m.settings_enabled)

        developer_frame = ttk.Frame(main_frame)
        developer_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(developer_frame,
                  text=languages[self.parent.save_m.data['language']]['settings']['settings_show_developer']).pack(
            side='left')
        self.developer_var = tk.StringVar(developer_frame)
        self.developer_var.set(self.parent.save_m.data['show_developer_menu'].capitalize())
        developer_dropdown = tk.OptionMenu(developer_frame, self.developer_var, *[
            languages[self.parent.save_m.data['language']]['settings']['setting_enabled'],
            languages[self.parent.save_m.data['language']]['settings']['setting_disabled']])
        developer_dropdown.pack(side='right')
        developer_dropdown.configure(state=self.parent.save_m.settings_enabled)

        help_frame = ttk.Frame(main_frame)
        help_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(help_frame,
                  text=languages[self.parent.save_m.data['language']]['settings']['settings_show_help']).pack(
            side='left')
        self.help_var = tk.StringVar(help_frame)
        self.help_var.set(self.parent.save_m.data['show_help_menu'].capitalize())
        help_dropdown = tk.OptionMenu(help_frame, self.help_var, *[
            languages[self.parent.save_m.data['language']]['settings']['setting_enabled'],
            languages[self.parent.save_m.data['language']]['settings']['setting_disabled']])
        help_dropdown.pack(side='right')
        help_dropdown.configure(state=self.parent.save_m.settings_enabled)

        users_frame = ttk.Frame(main_frame)
        users_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(users_frame,
                  text=languages[self.parent.save_m.data['language']]['settings']['settings_show_users']).pack(
            side='left')
        self.users_var = tk.StringVar(users_frame)
        self.users_var.set(self.parent.save_m.data['show_users_menu'].capitalize())
        users_dropdown = tk.OptionMenu(users_frame, self.users_var, *[
            languages[self.parent.save_m.data['language']]['settings']['setting_enabled'],
            languages[self.parent.save_m.data['language']]['settings']['setting_disabled']])
        users_dropdown.pack(side='right')
        users_dropdown.configure(state=self.parent.save_m.settings_enabled)

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

        self.parent.save_m.data['automatic_update_check'] = self.update_var.get().lower()
        self.parent.save_m.data['theme'] = self.theme_var.get().lower()
        self.parent.save_m.data['show_checkout_menu'] = self.developer_var.get().lower()
        self.parent.save_m.data['show_developer_menu'] = self.developer_var.get().lower()
        self.parent.save_m.data['show_help_menu'] = self.help_var.get().lower()
        self.parent.save_m.data['show_users_menu'] = self.users_var.get().lower()

        self.parent.save_m.push_save()
        self.parent.menu_bar.generate()

        self.parent.tab_controller.select(0)
        self.destroy()
