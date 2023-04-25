import logging
import tkinter as tk
from tkinter import ttk

from languages import *
from popup_window import PopupWindow


class CheckinScreen(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw', fill='both', expand=True)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(side='top', fill='both')

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side='bottom', expand=True, fill='both')

        heading_frame = ttk.Frame(top_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text=languages[self.parent.save_m.data['language']]['checking']['checkin_heading'],
                  font=self.parent.heading_font).pack(
            side='left')

        barcode_frame = ttk.Frame(top_frame)
        barcode_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(barcode_frame,
                  text=languages[self.parent.save_m.data['language']]['checking']['checkout_item_barcode']).pack(
            side='left')
        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side='left')
        self.barcode_entry.bind('<Return>', lambda event: self.check_item_in())

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
        button_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_deny'],
                   command=lambda: [self.parent.tab_controller.select(0), self.destroy()]).pack(side='right')
        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['checking']['checkin_return'],
                   command=lambda: [self.check_item_in()]).pack(
            side='right')

        self.barcode_entry.focus()

    def check_item_in(self):
        self.parent.db.dbCursor.execute(f"""
            SELECT * FROM checkouts
            WHERE item_barcode='{self.barcode_entry.get()}'
        """)
        items = self.parent.db.dbCursor.fetchall()

        if len(items) == 1:

            self.parent.db.dbCursor.execute(f"""
                DELETE FROM checkouts
                WHERE item_barcode='{self.barcode_entry.get()}'
            """)
            self.parent.db.dbConnection.commit()

            logging.info(f'Checked in item with barcode {self.barcode_entry.get()}')

            self.parent.db.dbCursor.execute("""
                SELECT title FROM item_record
                WHERE id=(
                    SELECT id FROM items
                    WHERE barcode=%s    
                )
            """, (self.barcode_entry.get(),))
            return_title = self.parent.db.dbCursor.fetchall()

            self.tree.insert('', tk.END, values=[self.barcode_entry.get(), return_title[0][0]])
            self.barcode_entry.delete(0, tk.END)
        else:
            PopupWindow(self.parent, "Not Checked Out", "That item does not exist or is not checked out.")
