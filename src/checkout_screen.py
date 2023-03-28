import tkinter as tk


class CheckoutScreen(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.title('Checkout')

        user_frame = tk.Frame(self)
        user_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=(self.parent.padding * 2,
                                                                                      self.parent.padding))
        tk.Label(user_frame, text='User Barcode').pack(side='left')
        self.user_barcode = tk.Entry(user_frame)
        self.user_barcode.pack(side='right')

        barcode_frame = tk.Frame(self)
        barcode_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        tk.Label(barcode_frame, text='Item Barcode').pack(side='left')
        self.barcode_entry = tk.Entry(barcode_frame)
        self.barcode_entry.pack(side='right')

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, padx=self.parent.padding * 2,
                          pady=(self.parent.padding, self.parent.padding * 2))
        tk.Button(button_frame, text='Checkout', command=lambda: self.checkout_to_user()).pack(side='left')
        tk.Button(button_frame, text='Cancel', command=lambda: self.destroy()).pack(side='right')

        self.mainloop()

    def checkout_to_user(self):
        data = (self.user_barcode.get(), self.barcode_entry.get())

        items = self.parent.db.dbCursor.execute(f"""
            SELECT * FROM inventory
            WHERE barcode='{data[1]}'
        """).fetchall()

        users = self.parent.db.dbCursor.execute(f"""
            SELECT * FROM users
            WHERE barcode='{data[0]}'
        """).fetchall()

        if len(items) == 1 and len(users) == 1:

            self.parent.db.dbCursor.execute("""
                INSERT INTO checkouts(user_barcode, item_barcode)
                VALUES (?, ?) 
            """, data)
            self.parent.db.dbConnection.commit()

        else:
            popup = tk.Toplevel()
            tk.Label(popup, text='The user or item barcode were invalid, or the item is already checked out.').pack()
            popup.mainloop()
