from location_template import LocationTemplate
import logging
import mysql.connector


class LocationManage(LocationTemplate):

    def __init__(self, parent, location_id):
        super().__init__(parent)

        self.location_id = location_id

        self.heading_label.configure(text=self.parent.get_region_text('location_manage'))
        self.func_button.configure(text=self.parent.get_region_text('location_save'),
                                   command=lambda: [self.update_entry()])
        self.barcode_entry.bind('<Return>', lambda event: [self.update_entry()])

        self.fill_info()

    def fill_info(self):
        self.parent.db.dbCursor.execute(f"""
            SELECT * FROM locations
            WHERE location_id=%s""", (self.location_id,))
        location_row = self.parent.db.dbCursor.fetchall()

        self.barcode_entry.insert(0, location_row[0][1])
        self.name_entry.insert(0, location_row[0][2])

    def update_entry(self):
        try:
            self.parent.db.dbCursor.execute(f"""
                        UPDATE locations 
                        SET barcode=%s, name=%s
                        WHERE location_id={self.location_id}""", self.get_all_entries())
            self.parent.db.dbConnection.commit()

            logging.info(f'Updated location with barcode {self.get_all_entries()[0]}')
            for tab in self.parent.tab_controller.tabs():
                tab_object = self.parent.tab_controller.nametowidget(tab)
                if callable(getattr(tab_object, 'refresh_table', None)):
                    tab_object.refresh_table()
                    self.parent.tab_controller.select(tab)
            self.destroy()
        except mysql.connector.errors.IntegrityError:
            self.barcode_in_use()
