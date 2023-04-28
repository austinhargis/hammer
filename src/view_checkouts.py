import logging
import tkinter as tk
from tkinter import ttk


class ViewCheckouts(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True)

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(main_frame,
                  text=self.parent.get_region_text('checkout_view'),
                  font=self.parent.heading_font).pack()

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        self.checkout_tree = ttk.Treeview(tree_frame, columns=('user_barcode', 'item_barcode', 'item_title'))
        self.checkout_tree['show'] = 'headings'
        self.checkout_tree['displaycolumns'] = ('user_barcode', 'item_barcode', 'item_title')

        self.checkout_tree_scroll = ttk.Scrollbar(tree_frame, command=self.checkout_tree.yview)
        self.checkout_tree.configure(yscrollcommand=self.checkout_tree_scroll.set)
        self.checkout_tree_scroll.pack(side='right', fill='both')

        self.get_checkouts()

        self.checkout_tree.heading('user_barcode',
                                   text=self.parent.get_region_text('checkout_user_barcode'))
        self.checkout_tree.heading('item_barcode',
                                   text=self.parent.get_region_text('checkout_item_barcode'))
        self.checkout_tree.heading('item_title',
                                   text=self.parent.get_region_text('checkout_item_title'))
        self.checkout_tree.pack(fill='both', expand=True, padx=self.parent.padding, pady=(self.parent.padding, 0))

        close_frame = ttk.Frame(main_frame)
        close_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Button(close_frame,
                   text=self.parent.get_region_text('prompt_exit'),
                   command=lambda: self.destroy()).pack()

    def get_checkouts(self):
        self.parent.db.dbCursor.execute("""
            SELECT * FROM checkouts
        """)
        checkouts = self.parent.db.dbCursor.fetchall()

        for checkout_index in range(len(checkouts)):
            self.parent.db.dbCursor.execute(f"""
                        SELECT id FROM items
                        WHERE barcode='{checkouts[checkout_index][1]}'
            """)
            checkout_ids = self.parent.db.dbCursor.fetchall()

            self.parent.db.dbCursor.execute(f"""
                SELECT title FROM item_record
                WHERE id=%s
            """, list(checkout_ids[0]))
            checkout_titles = self.parent.db.dbCursor.fetchall()

            checkout_ = [checkouts[checkout_index][0], checkouts[checkout_index][1], checkout_titles[0][0]]

            self.checkout_tree.insert('', tk.END, values=checkout_)

            logging.info('Got list of all checkouts')
