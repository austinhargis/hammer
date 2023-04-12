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

    def get_all_data(self):
        return [self.barcode_entry.get(),
                self.first_name_entry.get(),
                self.last_name_entry.get()]
