import tkinter as tk
from tkinter import ttk

from popup_window import PopupWindow
from user_manage import ManageUser


class ViewSpecificUser(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.window()

    def window(self):

        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=self.parent.padding, pady=self.parent.padding)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill='both', side='top')

        left_frame = ttk.Frame(top_frame)
        left_frame.pack(expand=True, fill='both', side='left')

        right_frame = ttk.Frame(top_frame)
        right_frame.pack(expand=True, fill='both', side='left')

        ttk.Label(right_frame, font=self.parent.heading_font).pack()

        self.barcode_label = ttk.Label(right_frame)
        self.barcode_label.pack(anchor='nw')

        self.name_label = ttk.Label(right_frame)
        self.name_label.pack(anchor='nw')

        self.birthday_label = ttk.Label(right_frame)
        self.birthday_label.pack(anchor='nw')

        self.email_label = ttk.Label(right_frame)
        self.email_label.pack(anchor='nw')

        self.creation_date_label = ttk.Label(right_frame)
        self.creation_date_label.pack(anchor='nw')

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(expand=True, fill='both', side='bottom')

        heading_frame = ttk.Frame(left_frame)
        heading_frame.pack(anchor='nw')
        ttk.Label(heading_frame, text=self.parent.get_region_text('user_specific'), font=self.parent.heading_font).pack(
            anchor='nw',
            padx=self.parent.padding,
            pady=self.parent.padding)

        barcode_frame = ttk.Frame(left_frame)
        barcode_frame.pack(anchor='nw', padx=self.parent.padding)
        ttk.Label(barcode_frame, text=self.parent.get_region_text('checkout_user_barcode')).pack(side='left')
        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side='left')
        self.barcode_entry.focus()
        self.barcode_entry.bind('<Return>', lambda event: self.get_user())

        tree_frame = ttk.Frame(bottom_frame)
        tree_frame.pack(side='top', fill='both', expand=True, pady=self.parent.padding)
        self.tree = ttk.Treeview(tree_frame, columns=('item_barcode', 'item_title', 'item_description'))
        self.tree['show'] = 'headings'
        self.tree['displaycolumns'] = ('item_barcode', 'item_title', 'item_description')

        self.tree_scroll = ttk.Scrollbar(tree_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.pack(side='right', fill='both')

        self.tree.heading('item_barcode',
                          text=self.parent.get_region_text('checkout_item_barcode'))
        self.tree.column('item_barcode', stretch=False)
        self.tree.heading('item_title',
                          text=self.parent.get_region_text('checkout_item_title'))
        self.tree.heading('item_description', text=self.parent.get_region_text('item_description'))
        self.tree.pack(fill='both', expand=True, padx=(self.parent.padding, 0), pady=(0, self.parent.padding))

        ttk.Button(bottom_frame,
                   text=self.parent.get_region_text('prompt_exit'),
                   command=lambda: [self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='right')
        self.manage_user_button = ttk.Button(bottom_frame,
                                             text=self.parent.get_region_text('user_manage'),
                                             command=lambda: self.parent.create_tab(ManageUser, 'Manage User',
                                                                                    self.barcode_entry.get()))
        self.manage_user_button.pack(side='right')
        self.manage_user_button.configure(state='disabled')

    def get_user(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.parent.db.dbCursor.execute("""
            SELECT barcode, item_record.title, items.description 
            FROM items
            INNER JOIN item_record ON items.id = item_record.id
            INNER JOIN checkouts ON items.barcode = checkouts.item_barcode
            WHERE user_barcode=%s
        """, (self.barcode_entry.get(),))
        checkouts = self.parent.db.dbCursor.fetchall()

        self.parent.db.dbCursor.execute("""
            SELECT first_name, last_name, birthday, email, creation_date FROM users
            WHERE barcode=%s
        """, (self.barcode_entry.get(),))
        user_information = self.parent.db.dbCursor.fetchall()

        for item in checkouts:
            self.tree.insert('', tk.END, values=item)

        if len(user_information) == 1:
            self.barcode_label.configure(text=f'Barcode: {self.barcode_entry.get()}')
            self.name_label.configure(text=f'Name: {user_information[0][0]} {user_information[0][1]}')
            self.birthday_label.configure(text=f'Birthday: {user_information[0][2]}')
            self.email_label.configure(text=f'Email: {user_information[0][3]}')
            self.creation_date_label.configure(text=f'Created: {user_information[0][4]}')

            if bool(self.parent.user_permissions['can_modify_users']):
                self.manage_user_button.configure(state='normal')
        else:
            PopupWindow(self.parent, 'No User Found',
                        'A user with that barcode does not exist. Please check that the barcode has'
                        'been entered correctly.')
