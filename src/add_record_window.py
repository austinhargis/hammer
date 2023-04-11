import logging
import sqlite3
from datetime import datetime

from languages import *
from popup_window import PopupWindow
from record_info_template import RecordInfoTemplate


class AddRecordWindow(RecordInfoTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.heading_label.configure(
            text=languages[self.parent.save_m.data['language']]['item_info']['item_add_heading'])
        self.func_button.configure(
            text=languages[self.parent.save_m.data['language']]['prompts']['prompt_add_item'],
            command=lambda: [self.create_record()])

        self.type_text.bind('<Return>', lambda event: self.create_record())

    def create_record(self):
        item_information = self.get_item_info()
        if item_information[0].replace(' ', '') == '':
            PopupWindow(self.parent, "Missing Field", "The title field must have a value specified "
                                                      "before this item can be added to the table.")

            return

        try:
            item_information = list(item_information)
            item_information.append(datetime.now())
            item_information.append(datetime.now())
            self.parent.db.dbCursor.execute(f"""INSERT INTO item_record(title, author, description, publish_date, type, creation_date, managed_date)
                                      VALUES (?, ?, ?, ?, ?, ?, ?)""", item_information)
            self.parent.db.dbConnection.commit()
            self.parent.refresh_table()

            logging.info(f'Created record {item_information[0]}')

            self.parent.tab_controller.select(0)
            self.destroy()

        except sqlite3.IntegrityError:
            self.parent.db.unique_conflict()
