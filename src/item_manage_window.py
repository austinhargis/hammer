import logging
import mysql.connector

from item_template import ItemTemplate


class ManageItemWindow(ItemTemplate):

    def __init__(self, parent, entry_id):
        super().__init__(parent, entry_id)

        self.entry_id = entry_id
        self.parent = parent

        self.heading_label.configure(text=self.parent.get_region_text('item_manage_heading'))
        self.func_button.configure(text=self.parent.get_region_text('prompt_save_changes'),
                                   command=lambda: self.update_item())

        self.insert_data()

        self.description_entry.bind('<Return>', lambda event: self.update_item())

    def insert_data(self):
        self.parent.db.dbCursor.execute(f"""
            SELECT barcode, location_barcode, description
            FROM items
            WHERE barcode=%s
        """, (self.entry_id,))
        data = self.parent.db.dbCursor.fetchone()

        self.barcode_entry.insert(0, data[0])
        self.location_entry.insert(0, data[1])
        self.description_entry.insert(0, data[2])

        self.barcode_entry.configure(state='disabled')

    def update_item(self):
        try:
            data = self.get_item_info()
            del data[:2]

            self.parent.db.dbCursor.execute(f"""
                UPDATE items
                SET location_barcode=%s, description=%s
                WHERE barcode='{self.entry_id}'
            """, data)
            self.parent.db.dbConnection.commit()

            logging.info(f'Updated item with id {self.entry_id}')

            for tab in self.parent.tab_controller.tabs():
                tab_object = self.parent.tab_controller.nametowidget(tab)
                if callable(getattr(tab_object, 'refresh_table', None)):
                    tab_object.refresh_table()
                    self.parent.tab_controller.select(tab)

            self.destroy()
        except mysql.connector.errors.IntegrityError:
            self.parent.db.unique_conflict()
