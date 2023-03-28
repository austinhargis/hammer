import tkinter as tk


class CreateUser(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.title('Add User')

        first_name_frame = tk.Frame(self)
        first_name_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=(self.parent.padding * 2,
                                                                                            self.parent.padding))
        tk.Label(first_name_frame, text='First Name').pack(side='left')
        first_name_entry = tk.Entry(first_name_frame)
        first_name_entry.pack(side='right')

        last_name_frame = tk.Frame(self)
        last_name_frame.pack(fill='both', expand=True, padx=self.parent.padding*2, pady=self.parent.padding)
        tk.Label(last_name_frame, text='Last Name').pack(side='left')
        last_name_entry = tk.Entry(last_name_frame)
        last_name_entry.pack(side='right')

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, padx=self.parent.padding * 2,
                          pady=(self.parent.padding, self.parent.padding * 2))
        tk.Button(button_frame, text='Add User', command=lambda: self.add_user([first_name_entry.get(), last_name_entry.get()])).pack(side='left')
        tk.Button(button_frame, text='Cancel', command=lambda: self.destroy()).pack(side='right')

        self.mainloop()

    def add_user(self, data):
        self.parent.db.dbCursor.execute(f"""
            INSERT INTO users(first_name, last_name) 
            VALUES (?, ?)""", data)
        self.parent.db.dbConnection.commit()
        self.destroy()
