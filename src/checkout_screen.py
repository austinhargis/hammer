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
        user_barcode = tk.Entry(user_frame)
        user_barcode.pack(side='right')

        barcode_frame = tk.Frame(self)
        barcode_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        tk.Label(barcode_frame, text='Item Barcode').pack(side='left')
        barcode_entry = tk.Entry(barcode_frame)
        barcode_entry.pack(side='right')

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, padx=self.parent.padding * 2,
                          pady=(self.parent.padding, self.parent.padding * 2))
        tk.Button(button_frame, text='Checkout').pack(side='left')
        tk.Button(button_frame, text='Cancel', command=lambda: self.destroy()).pack(side='right')

        self.mainloop()
