import logging
import sqlite3

from location_template import LocationTemplate
from popup_window import PopupWindow


class LocationManage(LocationTemplate):

    def __init__(self, parent, location_id):
        super().__init__(parent)

        self.location_id = location_id

        self.heading_label.configure(text='Manage Location')
        self.func_button.configure(text='Save Location',
                                   command=lambda: [self.update_entry()])

        self.fill_info()

    def fill_info(self):
        location_row = self.parent.db.dbCursor.execute(f"""
                    SELECT * FROM locations
                    WHERE location_id=?""", (self.location_id,)).fetchall()

        self.barcode_entry.insert(0, location_row[0][1])
        self.name_entry.insert(0, location_row[0][2])

    def update_entry(self):
        try:
            self.parent.db.dbCursor.execute(f"""
                        UPDATE locations 
                        SET barcode=?, name=?
                        WHERE location_id={self.location_id}""", self.get_all_entries())
            self.parent.db.dbConnection.commit()

            logging.info(f'Updated location with barcode {self.get_all_entries()[0]}')

            self.parent.tab_controller.select(0)
            self.destroy()

        except sqlite3.IntegrityError:
            PopupWindow(self.parent, 'Barcode in Use', 'This barcode is already in use. Please try another.')
