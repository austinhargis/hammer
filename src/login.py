import logging

import bcrypt
from tkinter import ttk

from home_tab import HomeTab
from popup_window import PopupWindow


class Login(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.password_entry = None
        self.user_barcode = None
        self.parent = parent

        self.window()

    def get_motd(self):
        self.parent.db.dbCursor.execute("""
            SELECT message FROM message_of_the_day
            ORDER BY id DESC
        """)
        message = self.parent.db.dbCursor.fetchone()

        logging.info('Got the message of the day')

        return message[0]

    def window(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(anchor='nw', expand=True, fill='both')

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(anchor='nw', fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text=self.parent.get_region_text('login_heading'),
                  font=self.parent.heading_font).pack(side='top', anchor='nw')
        ttk.Label(heading_frame, text=f"{self.get_motd()}", font=('Arial', 14),
                  wraplength=self.parent.wraplength).pack(anchor='nw',
                                                          side='top')

        user_frame = ttk.Frame(main_frame)
        user_frame.pack(anchor='nw', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(user_frame,
                  text=self.parent.get_region_text('username')).pack(
            side='left')
        self.user_barcode = ttk.Entry(user_frame)
        self.user_barcode.pack(side='left', ipadx=16)

        password_frame = ttk.Frame(main_frame)
        password_frame.pack(anchor='nw', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(password_frame,
                  text=self.parent.get_region_text('password')).pack(
            side='left')
        self.password_entry = ttk.Entry(password_frame, show='*')
        self.password_entry.pack(side='left', ipadx=16)

        ttk.Button(main_frame, command=lambda: self.password_check(),
                   text=self.parent.get_region_text('login_heading')).pack(padx=self.parent.padding, anchor='nw')

        self.user_barcode.focus()
        self.user_barcode.bind('<Return>', lambda event: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda event: self.password_check())

    def password_check(self):
        self.parent.db.dbCursor.execute("""SELECT password FROM users WHERE barcode=%s""", (self.user_barcode.get(),))
        password = self.parent.db.dbCursor.fetchall()

        user_password = self.password_entry.get().encode('utf-8')

        try:
            if bcrypt.checkpw(user_password, password[0][0].encode('utf-8')):
                self.parent.user_barcode = self.user_barcode.get()
                self.parent.get_user_permissions()
                self.parent.create_tab(HomeTab, self.parent.get_region_text('home_tab'))
                self.parent.home_tab = self.parent.tab_controller.nametowidget('.!hometab')
                self.destroy()
            else:
                raise IndexError
        except IndexError:
            PopupWindow(self.parent, self.parent.get_region_text('login_error_title'),
                        self.parent.get_region_text('login_error_body'))
