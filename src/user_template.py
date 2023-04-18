import tkinter as tk
from tkinter import ttk

from languages import *


class UserTemplate(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        self.title_label = ttk.Label(title_frame,
                                     font=self.parent.heading_font)
        self.title_label.pack(side='left')

        barcode_frame = ttk.Frame(main_frame)
        barcode_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(barcode_frame,
                  text=languages[self.parent.save_m.data['language']]['users']['user_barcode']).pack(side='left')
        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side='right')

        first_name_frame = ttk.Frame(main_frame)
        first_name_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(first_name_frame, text=languages[self.parent.save_m.data['language']]['users']['user_first_name']) \
            .pack(side='left')
        self.first_name_entry = ttk.Entry(first_name_frame)
        self.first_name_entry.pack(side='right')

        last_name_frame = ttk.Frame(main_frame)
        last_name_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(last_name_frame, text=languages[self.parent.save_m.data['language']]['users']['user_last_name']) \
            .pack(side='left')
        self.last_name_entry = ttk.Entry(last_name_frame)
        self.last_name_entry.pack(side='right')

        birthday_frame = ttk.Frame(main_frame)
        birthday_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(birthday_frame, text='Birthday').pack(side='left')
        self.birthday_entry = ttk.Entry(birthday_frame)
        self.birthday_entry.pack(side='right')

        email_frame = ttk.Frame(main_frame)
        email_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(email_frame, text='Email').pack(side='left')
        self.email_entry = ttk.Entry(email_frame)
        self.email_entry.pack(side='right')

        self.check_out_value = tk.StringVar(value='disallowed')
        check_out_frame = ttk.Frame(main_frame)
        check_out_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        self.check_out_check = ttk.Checkbutton(check_out_frame,
                                               text='Allow Checkouts',
                                               variable=self.check_out_value,
                                               onvalue='allowed',
                                               offvalue='disallowed')
        self.check_out_check.pack(side='left')

        self.manage_item_value = tk.StringVar(value='disallowed')
        manage_item_frame = ttk.Frame(main_frame)
        manage_item_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        self.manage_item_check = ttk.Checkbutton(manage_item_frame,
                                                 text='Allow Item Management',
                                                 variable=self.manage_item_value,
                                                 onvalue='allowed',
                                                 offvalue='disallowed')
        self.manage_item_check.pack(side='left')

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(expand=True, padx=self.parent.padding,
                          pady=(0, self.parent.padding))
        self.confirm_button = ttk.Button(button_frame)
        self.confirm_button.pack(side='left')
        ttk.Button(button_frame, text=languages[self.parent.save_m.data['language']]['prompts']['prompt_deny'],
                   command=lambda: [self.parent.tab_controller.select(0), self.destroy()]).pack(side='right')

        self.barcode_entry.focus()
        self.barcode_entry.bind('<Return>', lambda event: self.first_name_entry.focus())
        self.first_name_entry.bind('<Return>', lambda event: self.last_name_entry.focus())
        self.last_name_entry.bind('<Return>', lambda event: self.birthday_entry.focus())
        self.birthday_entry.bind('<Return>', lambda event: self.email_entry.focus())

    def get_all_data(self):
        return [self.barcode_entry.get(),
                self.first_name_entry.get(),
                self.last_name_entry.get(),
                self.birthday_entry.get(),
                self.email_entry.get(),
                self.manage_item_value.get(),
                self.check_out_value.get()]
