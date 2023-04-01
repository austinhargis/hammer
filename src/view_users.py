import sqlite3
import tkinter as tk
from tkinter import ttk


class ViewUsers(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.user_tree = ttk.Treeview(self, columns=('user_id', 'barcode', 'first_name', 'last_name'))
        self.user_tree['show'] = 'headings'
        self.user_tree['displaycolumns'] = ('barcode', 'first_name', 'last_name')

        self.user_tree_scroll = ttk.Scrollbar(self)
        self.user_tree_scroll.configure(command=self.user_tree.yview_scroll)
        self.user_tree.configure(yscrollcommand=self.user_tree_scroll.set)
        self.user_tree_scroll.pack(side='right', fill='both')

        self.get_users()

        self.user_tree.heading('user_id', text='ID')
        self.user_tree.heading('barcode', text='Barcode')
        self.user_tree.heading('first_name', text='First Name')
        self.user_tree.heading('last_name', text='Last Name')
        self.user_tree.pack(fill='both', expand=True, padx=self.parent.padding*2, pady=self.parent.padding*2)

    def get_users(self):
        users = self.parent.db.dbCursor.execute("""
            SELECT * FROM users
        """).fetchall()

        for user_index in range(len(users)):
            self.user_tree.insert('', tk.END, values=users[user_index])
