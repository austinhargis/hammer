import logging
import mysql.connector.errors
import tkinter as tk
from tkinter import ttk

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
            WHERE id=%s
        """, (self.entry_id,))
        data = self.parent.db.dbCursor.fetchone()

        self.barcode_entry.insert(0, data[0])
        self.location_entry.insert(0, data[1])
        self.description_entry.insert(0, data[2])

    def update_item(self):
        try:
            data = self.get_item_info()
            del data[0]

            if data[0] != '':
                self.parent.db.dbCursor.execute(f"""
                    UPDATE items
                    SET barcode=%s, location_barcode=%s, description=%s
                    WHERE id={self.entry_id}
                """, data)
                self.parent.db.dbConnection.commit()

                logging.info(f'Updated item with id {self.entry_id}')

                for tab in self.parent.tab_controller.tabs():
                    tab_object = self.parent.tab_controller.nametowidget(tab)
                    if callable(getattr(tab_object, 'refresh_table', None)):
                        tab_object.refresh_table()
                        self.parent.tab_controller.select(tab)

                self.destroy()

            else:
                raise mysql.connector.errors.IntegrityError

        except mysql.connector.errors.IntegrityError:
            self.parent.db.unique_conflict()
