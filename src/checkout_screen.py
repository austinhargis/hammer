import logging
import mysql.connector
import tkinter as tk
from tkinter import ttk

from languages import *
from popup_window import PopupWindow


class CheckoutScreen(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw', fill='both', expand=True)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(side='top', fill='both')

        left_frame = ttk.Frame(top_frame)
        left_frame.pack(expand=True, fill='x', side='left', anchor='nw')

        right_frame = ttk.Frame(top_frame)
        right_frame.pack(expand=True, fill='x', side='left', anchor='nw')

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side='bottom', expand=True, fill='both')

        user_heading_frame = ttk.Frame(right_frame)
        user_heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(user_heading_frame, text='User', font=self.parent.heading_font).pack(side='left')

        user_name_frame = ttk.Frame(right_frame)
        user_name_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.user_name = ttk.Label(user_name_frame, text='User: ')
        self.user_name.pack(side='left')

        user_checkouts = ttk.Frame(right_frame)
        user_checkouts.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.user_checkouts = ttk.Label(user_checkouts, text='Checkouts: ')
        self.user_checkouts.pack(side='left')

        heading_frame = ttk.Frame(left_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text=languages[self.parent.save_m.data['language']]['checking']['checkout_heading'],
                  font=self.parent.heading_font).pack(side='left', anchor='nw')

        user_frame = ttk.Frame(left_frame)
        user_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(user_frame,
                  text=languages[self.parent.save_m.data['language']]['checking']['checkout_user_barcode']).pack(
            side='left')
        self.user_barcode = ttk.Entry(user_frame)
        self.user_barcode.pack(side='left')

        barcode_frame = ttk.Frame(left_frame)
        barcode_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(barcode_frame,
                  text=languages[self.parent.save_m.data['language']]['checking']['checkout_item_barcode']).pack(
            side='left')
        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side='left')

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

        button_frame = ttk.Frame(bottom_frame)
        button_frame.pack(anchor='s', side='bottom', fill='both', padx=self.parent.padding,
                          pady=(0, self.parent.padding))
        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_exit'],
                   command=lambda: [self.parent.tab_controller.select(0), self.destroy()]).pack(side='right')
        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['checking']['checkout_confirm'],
                   command=lambda: [self.parent.db.dbConnection.commit(), self.parent.tab_controller.select(0)]) \
            .pack(side='right')

        self.user_barcode.focus()
        self.barcode_entry.bind('<Return>', lambda event: self.checkout_to_user())
        self.user_barcode.bind('<Return>', lambda event: self.get_user())

    def checkout_to_user(self):
        data = (self.user_barcode.get(), self.barcode_entry.get())

        # Get a list of all items with that item barcode
        self.parent.db.dbCursor.execute(f"""
            SELECT * FROM items
            WHERE barcode='{data[1]}'
        """)
        items = self.parent.db.dbCursor.fetchall()

        # Get a list of all users with that user barcode
        self.parent.db.dbCursor.execute(f"""
            SELECT * FROM users
            WHERE barcode=%s
        """, (data[0],))
        users = self.parent.db.dbCursor.fetchall()

        if len(items) == 1 and len(users) == 1:

            try:
                self.parent.db.dbCursor.execute("""
                    INSERT INTO checkouts(user_barcode, item_barcode)
                    VALUES (%s, %s) 
                """, data)

                self.parent.db.dbConnection.commit()

                logging.info(f'Checked out item with barcode {data[1]} to user with barcode {data[0]}')
                self.update_tree()
                self.barcode_entry.delete(0, tk.END)

            except mysql.connector.errors.IntegrityError:
                PopupWindow(self.parent, "Already Checked Out", "This item is already checked out to a user. "
                                                                "This checkout cannot be completed at this time.")
                logging.info(f'Item with barcode {data[1]} is already checked out')

        else:
            PopupWindow(self.parent, "Invalid Barcode", "The user or item barcode were invalid or do not exist.")
            logging.info(f'One or both barcode(s) are invalid')

    def get_user(self):
        self.parent.db.dbCursor.execute("""
            SELECT * FROM users
            WHERE barcode=%s    
        """, (self.user_barcode.get(),))
        user = self.parent.db.dbCursor.fetchall()

        self.user_name.configure(text=f'User: {user[0][2]} {user[0][3]}')

        self.parent.db.dbCursor.execute("""
            SELECT * FROM checkouts
            WHERE user_barcode=%s
        """, (self.user_barcode.get(),))
        checkouts = self.parent.db.dbCursor.fetchall()

        if user[0][5] == 'disallowed':
            self.barcode_entry.configure(state='disabled')
            PopupWindow(self.parent, 'Checkout Not Permitted', 'You are not presently allowed to checkout items. '
                                                               'If you think this is a mistake, please contact an adminstrator.')
        else:
            self.barcode_entry.configure(state='normal')
            self.barcode_entry.focus()

        self.user_checkouts.configure(text=f'Checkouts: {len(checkouts)}')

    def update_tree(self):
        self.parent.db.dbCursor.execute("""
            SELECT title from item_record
            WHERE id=(
                SELECT id FROM items
                WHERE barcode=%s)
        """, (self.barcode_entry.get(),))
        title_row = self.parent.db.dbCursor.fetchall()

        self.tree.insert('', tk.END, values=[self.barcode_entry.get(), title_row[0][0]])
