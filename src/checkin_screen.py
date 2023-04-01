import tkinter as tk
from tkinter import ttk


class CheckinScreen(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        barcode_frame = tk.Frame(self)
        barcode_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(barcode_frame, text='Item Barcode').pack(side='left')
        self.barcode_entry = tk.Entry(barcode_frame)
        self.barcode_entry.pack(side='right')

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, padx=self.parent.padding,
                          pady=(0, self.parent.padding))
        ttk.Button(button_frame, text='Return Item', command=lambda: self.check_item_in()).pack(side='left')
        ttk.Button(button_frame, text='Cancel', command=lambda: self.destroy()).pack(side='right')

    def check_item_in(self):
        items = self.parent.db.dbCursor.execute(f"""
            SELECT * FROM checkouts
            WHERE item_barcode='{self.barcode_entry.get()}'
        """).fetchall()

        if len(items) == 1:

            self.parent.db.dbCursor.execute(f"""
                DELETE FROM checkouts
                WHERE item_barcode='{self.barcode_entry.get()}'
            """)
            self.parent.db.dbConnection.commit()

            popup = tk.Toplevel(padx=self.parent.padding, pady=self.parent.padding)
            ttk.Label(popup,
                     text='The item was successfully checked in.',
                     wraplength=self.parent.wraplength,
                     justify='center').pack()
            ttk.Button(popup, text='Okay', command=lambda: [popup.destroy(), self.destroy()])\
                .pack()

            popup.mainloop()

        else:
            popup = tk.Toplevel(padx=self.parent.padding, pady=self.parent.padding)
            ttk.Label(popup,
                     text='That item does not exist or is not checked out.',
                     wraplength=self.parent.wraplength,
                     justify='center').pack()
            ttk.Button(popup, text='Okay', command=lambda: popup.destroy()).pack()

            popup.mainloop()
