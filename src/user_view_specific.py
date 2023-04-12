import tkinter as tk
from tkinter import ttk

from user_manage import ManageUser


class ViewSpecificUser(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.window()

    def window(self):

        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both')

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(expand=True, fill='both', side='top')

        left_frame = ttk.Frame(top_frame)
        left_frame.pack(expand=True, fill='both', side='left')

        right_frame = ttk.Frame(top_frame)
        right_frame.pack(expand=True, fill='both', side='left')

        self.name_label = ttk.Label(right_frame)
        self.name_label.pack(anchor='nw')

        self.creation_date_label = ttk.Label(right_frame)
        self.creation_date_label.pack(anchor='nw')

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(expand=True, fill='both', side='bottom')

        heading_frame = ttk.Frame(left_frame)
        heading_frame.pack(anchor='nw')
        ttk.Label(heading_frame, text='View User', font=self.parent.heading_font).pack(anchor='nw',
                                                                                       padx=self.parent.padding,
                                                                                       pady=self.parent.padding)

        barcode_frame = ttk.Frame(left_frame)
        barcode_frame.pack(anchor='nw', padx=self.parent.padding)
        ttk.Label(barcode_frame, text='User Barcode').pack(side='left')
        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side='left')
        self.barcode_entry.focus()
        self.barcode_entry.bind('<Return>', lambda event: self.get_user())

        tree_frame = ttk.Frame(bottom_frame)
        tree_frame.pack(side='top', fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        self.tree = ttk.Treeview(tree_frame, columns=('item_barcode', 'item_title'))
        self.tree['show'] = 'headings'
        self.tree['displaycolumns'] = ('item_barcode', 'item_title')

        self.tree_scroll = ttk.Scrollbar(tree_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.pack(side='right', fill='both', pady=self.parent.padding)

        self.tree.heading('item_barcode',
                          text='Item Barcode')
        self.tree.heading('item_title',
                          text='Item Title')
        self.tree.pack(fill='both', expand=True, padx=(self.parent.padding, 0), pady=(0, self.parent.padding))

        ttk.Button(bottom_frame,
                   text='Manage User',
                   command=lambda: self.parent.create_tab(ManageUser, 'Manage User', self.barcode_entry.get())).pack()
        ttk.Button(bottom_frame,
                   text='Close',
                   command=lambda: [self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='bottom', pady=(0, self.parent.padding))

    def get_user(self):
        checkouts = self.parent.db.dbCursor.execute("""
            SELECT barcode, item_record.title 
            FROM items
            INNER JOIN item_record ON items.id = item_record.id
            INNER JOIN checkouts ON items.barcode = checkouts.item_barcode
            WHERE user_barcode=?
        """, (self.barcode_entry.get(),)).fetchall()

        user_information = self.parent.db.dbCursor.execute("""
            SELECT first_name, last_name, creation_date FROM users
            WHERE barcode=?
        """, (self.barcode_entry.get(),)).fetchall()

        for item in checkouts:
            self.tree.insert('', tk.END, values=item)

        if len(user_information) == 1:
            self.name_label.configure(text=f'Name: {user_information[0][0]} {user_information[0][1]}')
            self.creation_date_label.configure(text=f'Created: {user_information[0][2]}')
