import sys
from tkinter import ttk


class ConfigureEnvWindow(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.host_entry = None
        self.pass_entry = None
        self.user_entry = None

        self.window()

    def write_to_env(self):
        message = f"""DB_HOST={self.host_entry.get()}\nDB_USER={self.user_entry.get()}\nDB_PASSWORD={self.pass_entry.get()}"""

        with open('./.env', 'w') as file:
            file.write(message)

        sys.exit()

    def window(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw', padx=5, pady=5)

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both')
        ttk.Label(heading_frame, text='Configure Database Credentials').pack(side='left')

        host_frame = ttk.Frame(main_frame)
        host_frame.pack(fill='both')
        ttk.Label(host_frame, text='Host Address').pack(side='left')
        self.host_entry = ttk.Entry(host_frame)
        self.host_entry.pack(side='right')

        user_frame = ttk.Frame(main_frame)
        user_frame.pack(fill='both')
        ttk.Label(user_frame, text='SQL Username').pack(side='left')
        self.user_entry = ttk.Entry(user_frame)
        self.user_entry.pack(side='right')

        pass_frame = ttk.Frame(main_frame)
        pass_frame.pack(fill='both')
        ttk.Label(pass_frame, text='SQL Password').pack(side='left')
        self.pass_entry = ttk.Entry(pass_frame)
        self.pass_entry.pack(side='right')

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='both')
        ttk.Button(button_frame, text='Save', command=lambda: self.write_to_env()).pack(side='left')
        ttk.Button(button_frame, text='Close', command=lambda: self.destroy()).pack(side='left')

        self.host_entry.bind('<Return>', lambda event: self.user_entry.focus())
        self.user_entry.bind('<Return>', lambda event: self.pass_entry.focus())
        self.pass_entry.bind('<Return>', lambda event: self.write_to_env())
