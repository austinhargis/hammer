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
        self.parent.db.dbCursor.execute(f"""
            DELETE FROM checkouts
            WHERE item_barcode='{self.barcode_entry.get()}'
        """)
        self.parent.db.dbConnection.commit()

        self.destroy()
