import logging
import tkinter as tk
from tkinter import ttk


class ViewUsers(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True)

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text=self.parent.get_region_text('user_view'),
                  font=self.parent.heading_font).pack()

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        self.user_tree = ttk.Treeview(tree_frame, columns=('user_id', 'barcode', 'first_name', 'last_name'))
        self.user_tree['show'] = 'headings'
        self.user_tree['displaycolumns'] = ('barcode', 'first_name', 'last_name')

        self.user_tree_scroll = ttk.Scrollbar(tree_frame, command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=self.user_tree_scroll.set)
        self.user_tree_scroll.pack(side='right', fill='both')

        self.get_users()

        self.user_tree.heading('user_id',
                               text=self.parent.get_region_text('user_id'))
        self.user_tree.heading('barcode',
                               text=self.parent.get_region_text('user_barcode'))
        self.user_tree.heading('first_name',
                               text=self.parent.get_region_text('user_first_name'))
        self.user_tree.heading('last_name',
                               text=self.parent.get_region_text('user_last_name'))
        self.user_tree.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))

        close_frame = ttk.Frame(main_frame)
        close_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Button(close_frame,
                   text=self.parent.get_region_text('prompt_exit'),
                   command=lambda: [self.parent.tab_controller.select(0),
                                    self.destroy()]).pack()

    def get_users(self):
        self.parent.db.dbCursor.execute("""
            SELECT * FROM users
        """)
        users = self.parent.db.dbCursor.fetchall()

        for user_index in range(len(users)):
            self.user_tree.insert('', tk.END, values=users[user_index])

        logging.info('Got list of all users')