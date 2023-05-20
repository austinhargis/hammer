from item_template import ItemTemplate
import logging
import mysql.connector
from tkinter import messagebox


class AddItemWindow(ItemTemplate):

    def __init__(self, parent, entry_id):
        super().__init__(parent, entry_id)

        self.parent = parent
        self.entry_id = entry_id

        self.heading_label.configure(text=self.parent.get_region_text('prompt_add_item_to_record'))
        self.func_button.configure(text=self.parent.get_region_text('prompt_add_item_to_record'),
                                   command=lambda: self.create_item())

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
                for tab in self.parent.tab_controller.tabs():
                    tab_object = self.parent.tab_controller.nametowidget(tab)
                    if hasattr(tab_object, 'id'):
                        if tab_object.id == self.entry_id:
                            tab_object.refresh_table()
                self.destroy()
            else:
                messagebox.showerror(title=self.parent.get_region_text('missing_barcode_title'),
                                     message=self.parent.get_region_text('missing_barcode_body'))
        except mysql.connector.errors.IntegrityError:
            self.parent.db.unique_conflict()
