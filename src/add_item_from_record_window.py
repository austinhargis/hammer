import logging
import sqlite3

from popup_window import PopupWindow
from record_child_template import RecordChildTemplate


class AddItemFromRecordWindow(RecordChildTemplate):

    def __init__(self, parent, entry_id):
        super().__init__(parent, entry_id)

        self.parent = parent
        self.entry_id = entry_id

        self.heading_label.configure(text='Create Item From Record')
        self.func_button.configure(text='Add Item to Record', command=lambda: self.create_item())

        self.description_entry.bind('<Return>', lambda event: self.create_item())

    def create_item(self):
        try:
            self.parent.db.dbCursor.execute("""
                SELECT * FROM locations
                WHERE barcode=%s
            """, (self.get_item_info()[2],))
            locations_with_barcode = self.parent.db.dbCursor.fetchall()

            if self.get_item_info()[1] != '' and len(locations_with_barcode) == 1:
                self.parent.db.dbCursor.execute("""
                    INSERT INTO items
                    VALUES (%s, %s, %s, %s)
                """, self.get_item_info())
                self.parent.db.dbConnection.commit()
                logging.info(f'Created item {self.get_item_info()[1]} from record {self.get_item_info()[0]}')
                self.destroy()
            else:
                PopupWindow(self.parent, 'Barcode Missing', 'Items must have a barcode in order to be created.')
        except sqlite3.IntegrityError:
            self.parent.db.unique_conflict()
