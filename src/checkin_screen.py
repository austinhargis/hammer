import tkinter as tk


class CheckinScreen(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.title('Checkin')

        barcode_frame = tk.Frame(self)
        barcode_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        tk.Label(barcode_frame, text='Item Barcode').pack(side='left')
        self.barcode_entry = tk.Entry(barcode_frame)
        self.barcode_entry.pack(side='right')

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, padx=self.parent.padding * 2,
                          pady=(self.parent.padding, self.parent.padding * 2))
        tk.Button(button_frame, text='Return Item', command=lambda: self.check_item_in()).pack(side='left')
        tk.Button(button_frame, text='Cancel', command=lambda: self.destroy()).pack(side='right')

        self.mainloop()

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

            confirmation_popup = tk.Toplevel()
            tk.Label(confirmation_popup, text='The item was successfully checked in.').pack()
            tk.Button(confirmation_popup, text='Okay', command=lambda: [confirmation_popup.destroy(), self.destroy()])\
                .pack()

            confirmation_popup.mainloop()

        else:
            not_exist_popup = tk.Toplevel()
            tk.Label(not_exist_popup, text='That item does not exist or is not checked out.').pack()
            tk.Button(not_exist_popup, text='Okay', command=lambda: not_exist_popup.destroy()).pack()

            not_exist_popup.mainloop()
