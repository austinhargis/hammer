import sqlite3
import tkinter as tk
from tkinter import ttk


class CheckoutScreen(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        title_frame = tk.Frame(self)
        title_frame.pack(fill='both', padx=self.parent.padding, pady=(self.parent.padding, 0))
        ttk.Label(title_frame, text='Checkout', font=self.parent.heading_font).pack(side='left')

        user_frame = tk.Frame(self)
        user_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(user_frame, text='User Barcode').pack(side='left')
        self.user_barcode = tk.Entry(user_frame)
        self.user_barcode.pack(side='left')

        barcode_frame = tk.Frame(self)
        barcode_frame.pack(fill='both', padx=self.parent.padding)
        ttk.Label(barcode_frame, text='Item Barcode').pack(side='left')
        self.barcode_entry = tk.Entry(barcode_frame)
        self.barcode_entry.pack(side='left')

        button_frame = tk.Frame(self)
        button_frame.pack(fill='both', padx=self.parent.padding,
                          pady=self.parent.padding)
        ttk.Button(button_frame, text='Checkout', command=lambda: self.checkout_to_user()).pack(side='left')
        ttk.Button(button_frame, text='Cancel', command=lambda: self.destroy()).pack(side='left')

    def checkout_to_user(self):
        data = (self.user_barcode.get(), self.barcode_entry.get())

        # Get a list of all items with that item barcode
        items = self.parent.db.dbCursor.execute(f"""
            SELECT * FROM inventory
            WHERE barcode='{data[1]}'
        """).fetchall()

        # Get a list of all users with that user barcode
        users = self.parent.db.dbCursor.execute(f"""
            SELECT * FROM users
            WHERE barcode='{data[0]}'
        """).fetchall()

        # Check that there is exactly one user and one item with the provided barcodes
        if len(items) == 1 and len(users) == 1:
            try:
                self.parent.db.dbCursor.execute("""
                    INSERT INTO checkouts(user_barcode, item_barcode)
                    VALUES (?, ?) 
                """, data)
                self.parent.db.dbConnection.commit()

                self.destroy()

            # Thrown if the item is already checked out to a user
            except sqlite3.IntegrityError:
                popup = tk.Toplevel(padx=self.parent.padding, pady=self.parent.padding)
                ttk.Label(popup,
                          text='This item is already checked out to a user. '
                               'This checkout cannot be completed at this time.',
                          wraplength=self.parent.wraplength,
                          justify='center').pack()
                ttk.Button(popup, text='Continue', command=lambda: popup.destroy()).pack()

                popup.mainloop()

        # If a user or item does not exist, throw a popup error
        else:
            popup = tk.Toplevel(padx=self.parent.padding, pady=self.parent.padding)
            ttk.Label(popup,
                      text='The user or item barcode were invalid.',
                      wraplength=self.parent.wraplength,
                      justify='center').pack()
            ttk.Button(popup, text='Continue', command=lambda: popup.destroy()).pack()

            popup.mainloop()
