import tkinter as tk
from tkinter import ttk


class ViewCheckouts(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.title('View Checkouts')

        self.checkout_tree = ttk.Treeview(self, columns=('user_barcode', 'item_barcode', 'item_title'))
        self.checkout_tree['show'] = 'headings'
        self.checkout_tree['displaycolumns'] = ('user_barcode', 'item_barcode', 'item_title')

        self.checkout_tree_scroll = ttk.Scrollbar(self)
        self.checkout_tree_scroll.configure(command=self.checkout_tree.yview_scroll)
        self.checkout_tree.configure(yscrollcommand=self.checkout_tree_scroll.set)
        self.checkout_tree_scroll.pack(side='right', fill='both')

        self.get_checkouts()

        self.checkout_tree.heading('user_barcode', text='User Barcode')
        self.checkout_tree.heading('item_barcode', text='Item Barcode')
        self.checkout_tree.heading('item_title', text='Item Title')
        self.checkout_tree.pack(fill='both', expand=True, padx=self.parent.padding*2, pady=self.parent.padding*2)

        self.mainloop()

    def get_checkouts(self):
        checkouts = self.parent.db.dbCursor.execute("""
            SELECT * FROM checkouts
        """).fetchall()

        for checkout_index in range(len(checkouts)):
            checkout_titles = self.parent.db.dbCursor.execute(f"""
                        SELECT title FROM inventory
                        WHERE barcode='{checkouts[checkout_index][1]}'
            """).fetchall()

            checkout_ = [checkouts[checkout_index][0], checkouts[checkout_index][1], checkout_titles[0][0]]

            self.checkout_tree.insert('', tk.END, values=checkout_)
