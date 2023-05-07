from datetime import datetime
import logging
import mysql.connector

from languages import *
from popup_window import PopupWindow
from record_info_template import RecordInfoTemplate


class AddRecordWindow(RecordInfoTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.heading_label.configure(
            text=self.parent.get_region_text('item_add_heading'))
        self.func_button.configure(
            text=self.parent.get_region_text('prompt_add_item'),
            command=lambda: [self.create_record()])

        self.type_text.bind('<Return>', lambda event: self.create_record())

    def create_record(self):
        item_information = self.get_item_info()
        if item_information[0].replace(' ', '') == '':
            PopupWindow(self.parent, self.parent.get_region_text('missing_item_title'),
                        self.parent.get_region_text('missing_item_body'))

            return

        try:
            item_information = list(item_information)
            item_information.append(datetime.now())
            item_information.append(datetime.now())
            self.parent.db.dbCursor.execute(f"""
                INSERT INTO item_record(title, author, description, publish_date, type, creation_date, managed_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""", item_information)
            self.parent.db.dbConnection.commit()
            self.parent.home_tab.refresh_table()

            logging.info(f'Created record {item_information[0]}')

            child = self.parent.tree.get_children()[len(self.parent.tree.get_children()) - 1]
            self.parent.tree.focus(child)
            self.parent.tree.selection_set(child)
            self.parent.tab_controller.select(0)
            self.destroy()

        except mysql.connector.errors.IntegrityError:
            self.parent.db.unique_conflict()
