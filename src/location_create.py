import sqlite3

from location_template import LocationTemplate
from popup_window import PopupWindow


class LocationCreate(LocationTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.heading_label.configure(text='Create Location')
        self.func_button.configure(text='Create Location',
                                   command=lambda: [self.create_query(),
                                                    self.destroy()])

    def create_query(self):
        try:
            self.parent.db.dbCursor.execute(f"""
                INSERT INTO locations (barcode, name)
                VALUES (?, ?)
            """, self.get_all_entries())
            self.parent.db.dbConnection.commit()
        except sqlite3.IntegrityError:
            PopupWindow(self.parent, 'Barcode in Use', 'This barcode is already in use. Please try another one.')