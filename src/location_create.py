import logging

import mysql.connector.errors

from location_template import LocationTemplate


class LocationCreate(LocationTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.heading_label.configure(text=self.parent.get_region_text('location_create'))
        self.func_button.configure(text=self.parent.get_region_text('location_create'),
                                   command=lambda: [self.create_query()])
        self.barcode_entry.bind('<Return>', lambda event: [self.create_query()])

    def create_query(self):
        try:
            self.parent.db.dbCursor.execute(f"""
                INSERT INTO locations (barcode, name)
                VALUES (%s, %s)
            """, self.get_all_entries())
            self.parent.db.dbConnection.commit()

            logging.info(f'Created location with barcode {self.get_all_entries()[0]}')

            self.parent.tab_controller.select(0)
            self.destroy()
        except mysql.connector.errors.IntegrityError:
            self.barcode_in_use()
