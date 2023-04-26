import bcrypt
from tkinter import ttk

from home_tab import HomeTab

class Login(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.window()

    def window(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw', fill='both', expand=True)

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text='Login Test',
                  font=self.parent.heading_font).pack(side='left', anchor='nw')

        user_frame = ttk.Frame(main_frame)
        user_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(user_frame,
                  text='Username').pack(
            side='left')
        self.user_barcode = ttk.Entry(user_frame)
        self.user_barcode.pack(side='left')

        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(password_frame,
                  text='Password').pack(
            side='left')
        self.password_entry = ttk.Entry(password_frame, show='*')
        self.password_entry.pack(side='left')

        ttk.Button(main_frame, command=lambda: self.password_check(), text='CONFIRM').pack()

    def password_check(self):
        self.parent.db.dbCursor.execute("""SELECT password FROM users WHERE barcode=%s""", (self.user_barcode.get(),))
        password = self.parent.db.dbCursor.fetchall()

        user_password = self.password_entry.get().encode('utf-8')
        hash_pass = bcrypt.hashpw(user_password, bcrypt.gensalt())

        if bcrypt.checkpw(user_password, password[0][0].encode('utf-8')):
            self.parent.create_tab(HomeTab, 'Home')
            self.destroy()
        else:
            print('they don\'t')
