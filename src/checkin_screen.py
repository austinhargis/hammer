import logging
import tkinter as tk
from tkinter import ttk

from languages import *
from popup_window import PopupWindow


class CheckinScreen(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text=languages[self.parent.save_m.data['language']]['checking']['checkin_heading'],
                  font=self.parent.heading_font).pack(
            side='left')

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
                   text=languages[self.parent.save_m.data['language']]['checking']['checkin_return'],
                   command=lambda: [self.check_item_in(), self.parent.tab_controller.select(0)]).pack(
            side='left')
        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_deny'],
                   command=lambda: [self.parent.tab_controller.select(0), self.destroy()]).pack(side='right')

        self.barcode_entry.focus()

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

            logging.info(f'Checked in item with barcode {self.barcode_entry.get()}')

            PopupWindow(self.parent, "Check In Successful", "The item was successfully checked in.")

            self.parent.tab_controller.select(0)
            self.destroy()
        else:
            PopupWindow(self.parent, "Not Checked Out", "That item does not exist or is not checked out.")
