import logging
import sqlite3
from tkinter import ttk

from popup_window import PopupWindow
from record_child_template import RecordChildTemplate


class AddItemFromRecordWindow(RecordChildTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.heading_label.configure(text='Create Item From Record')
        self.func_button.configure(text='Add Item to Record', command=lambda: self.create_item())

    def create_item(self):
        try:
            locations_with_barcode = self.parent.db.dbCursor.execute("""
                SELECT * FROM locations
                WHERE barcode=?
            """, (self.get_item_info()[2],)).fetchall()

            if self.get_item_info()[1] != '' and len(locations_with_barcode) == 1:
                self.parent.db.dbCursor.execute("""
                    INSERT INTO items
                    VALUES (?, ?, ?, ?)
                """, self.get_item_info())
                self.parent.db.dbConnection.commit()
                logging.info(f'Created item {self.get_item_info()[1]} from record {self.get_item_info()[0]}')
                self.destroy()
            else:
                PopupWindow(self.parent, 'Barcode Missing', 'Items must have a barcode in order to be created.')
        except sqlite3.IntegrityError:
            self.parent.db.unique_conflict()
