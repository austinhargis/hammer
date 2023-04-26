from tkinter import ttk

from database import Database

class ConfigureEnvWindow(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.window()

    def write_to_env(self):
        message = f"""db_host={self.host_entry.get()}
        db_user={self.user_entry.get()}
        db_password={self.pass_entry.get()}"""

        data_out = open('./.env', 'w')
        data_out.write(message)
        data_out.close()

        self.parent.db = Database(self.parent)

    def window(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both')
        ttk.Label(heading_frame, font=self.parent.heading_font).pack(side='left')

        host_frame = ttk.Frame(main_frame)
        host_frame.pack(fill='both')
        ttk.Label(host_frame, text='Location Name').pack(side='left')
        self.host_entry = ttk.Entry(host_frame)
        self.host_entry.pack(side='right')

        user_frame = ttk.Frame(main_frame)
        user_frame.pack(fill='both')
        ttk.Label(user_frame, text='Barcode').pack(side='left')
        self.user_entry = ttk.Entry(user_frame)
        self.user_entry.pack(side='right')

        pass_frame = ttk.Frame(main_frame)
        pass_frame.pack(fill='both')
        ttk.Label(pass_frame, text='Barcode').pack(side='left')
        self.pass_entry = ttk.Entry(pass_frame)
        self.pass_entry.pack(side='right')

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='both')
        ttk.Button(button_frame, text='Save', command=lambda: self.write_to_env()).pack(side='left')
        ttk.Button(button_frame, text='Close', command=lambda: [self.parent.tab_controller.select(0),
                                                                self.destroy()]).pack(side='left')