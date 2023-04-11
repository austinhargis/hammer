import logging
import sqlite3
import tkinter as tk
from tkinter import ttk

from languages import *
from popup_window import PopupWindow


class CheckoutScreen(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text=languages[self.parent.save_m.data['language']]['checking']['checkout_heading'],
                  font=self.parent.heading_font).pack(side='left')

        user_frame = ttk.Frame(main_frame)
        user_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(user_frame,
                  text=languages[self.parent.save_m.data['language']]['checking']['checkout_user_barcode']).pack(
            side='left')
        self.user_barcode = ttk.Entry(user_frame)
        self.user_barcode.pack(side='right')

        barcode_frame = ttk.Frame(main_frame)
        barcode_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(barcode_frame,
                  text=languages[self.parent.save_m.data['language']]['checking']['checkout_item_barcode']).pack(
            side='left')
        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side='right')

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['checking']['checkout_confirm'],
                   command=lambda: [self.checkout_to_user(), self.parent.tab_controller.select(0)]).pack(side='left')
        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_deny'],
                   command=lambda: [self.parent.tab_controller.select(0), self.destroy()]).pack(side='right')

    def checkout_to_user(self):
        data = (self.user_barcode.get(), self.barcode_entry.get())

        # Get a list of all items with that item barcode
        items = self.parent.db.dbCursor.execute(f"""
            SELECT * FROM items
            WHERE barcode='{data[1]}'
        """).fetchall()

        # Get a list of all users with that user barcode
        users = self.parent.db.dbCursor.execute(f"""
            SELECT * FROM users
            WHERE barcode=?
        """, (data[0],)).fetchall()

        if len(items) == 1 and len(users) == 1:

            try:
                self.parent.db.dbCursor.execute("""
                    INSERT INTO checkouts(user_barcode, item_barcode)
                    VALUES (?, ?) 
                """, data)
                self.parent.db.dbConnection.commit()
                PopupWindow(self.parent, 'Checkout Successful', 'Your checkout was successful.')

                logging.info(f'Checked out item with barcode {data[1]} to user with barcode {data[0]}')

                self.parent.tab_controller.select(0)
                self.destroy()

            except sqlite3.IntegrityError:
                PopupWindow(self.parent, "Already Checked Out", "This item is already checked out to a user. "
                                                                "This checkout cnanot be completed at this time.")
                logging.info(f'Item with barcode {data[1]} is already checked out')

        else:
            PopupWindow(self.parent, "Invalid Barcode", "The user or item barcode were invalid or do not exist.")
            logging.info(f'One or both barcode(s) are invalid')
