import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import ttk


class CreateUser(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        barcode_frame = tk.Frame(self)
        barcode_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=(self.parent.padding * 2,
                                                                                         self.parent.padding))
        ttk.Label(barcode_frame, text='User Barcode').pack(side='left')
        barcode_entry = tk.Entry(barcode_frame)
        barcode_entry.pack(side='right')

        first_name_frame = tk.Frame(self)
        first_name_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(first_name_frame, text='First Name').pack(side='left')
        first_name_entry = tk.Entry(first_name_frame)
        first_name_entry.pack(side='right')

        last_name_frame = tk.Frame(self)
        last_name_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(last_name_frame, text='Last Name').pack(side='left')
        last_name_entry = tk.Entry(last_name_frame)
        last_name_entry.pack(side='right')

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, padx=self.parent.padding * 2,
                          pady=(self.parent.padding, self.parent.padding * 2))
        ttk.Button(button_frame, text='Add User',
                   command=lambda: self.add_user(
                       [barcode_entry.get(), first_name_entry.get(), last_name_entry.get()])).pack(side='left')
        ttk.Button(button_frame, text='Cancel', command=lambda: [self.parent.tab_controller.select(0),
                                                                 self.destroy()]).pack(side='right')

    def add_user(self, data):
        try:
            data.append(datetime.now())
            self.parent.db.dbCursor.execute(f"""
                INSERT INTO users(barcode, first_name, last_name, creation_date) 
                VALUES (?, ?, ?, ?)""", data)
            self.parent.db.dbConnection.commit()
            self.parent.tab_controller.select(0)
            self.destroy()
        except sqlite3.IntegrityError:
            self.parent.db.unique_conflict()
