import sqlite3
import tkinter as tk
from tkinter import ttk

from languages import *


class ViewUsers(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = tk.Frame(self)
        main_frame.pack(fill='both', expand=True)

        heading_frame = tk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text=languages[self.parent.save_m.data['language']]['users']['user_view'],
                  font=self.parent.heading_font).pack()

        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        self.user_tree = ttk.Treeview(tree_frame, columns=('user_id', 'barcode', 'first_name', 'last_name'))
        self.user_tree['show'] = 'headings'
        self.user_tree['displaycolumns'] = ('barcode', 'first_name', 'last_name')

        self.user_tree_scroll = ttk.Scrollbar(tree_frame, command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=self.user_tree_scroll.set)
        self.user_tree_scroll.pack(side='right', fill='both')

        self.get_users()

        self.user_tree.heading('user_id',
                               text=languages[self.parent.save_m.data['language']]['users']['user_id'])
        self.user_tree.heading('barcode',
                               text=languages[self.parent.save_m.data['language']]['users']['user_barcode'])
        self.user_tree.heading('first_name',
                               text=languages[self.parent.save_m.data['language']]['users']['user_first_name'])
        self.user_tree.heading('last_name',
                               text=languages[self.parent.save_m.data['language']]['users']['user_last_name'])
        self.user_tree.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))

        close_frame = tk.Frame(main_frame)
        close_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Button(close_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_exit'],
                   command=lambda: self.destroy()).pack()

    def get_users(self):
        users = self.parent.db.dbCursor.execute("""
            SELECT * FROM users
        """).fetchall()

        for user_index in range(len(users)):
            self.user_tree.insert('', tk.END, values=users[user_index])
