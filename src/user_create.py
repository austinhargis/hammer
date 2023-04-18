import logging
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from languages import *
from user_template import UserTemplate


class CreateUser(UserTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title_label.configure(text=languages[self.parent.save_m.data['language']]['users'][
            'user_create_heading'])

        self.confirm_button.configure(
            text=languages[self.parent.save_m.data['language']]['users']['user_create_heading'],
            command=lambda: self.add_user())

        self.email_entry.bind('<Return>', lambda event: self.add_user())

    def add_user(self):
        try:
            data = self.get_all_data()
            data.append(datetime.now())

            if data[0][0:1] == 'U' and data[1] != '':
                self.parent.db.dbCursor.execute(f"""
                    INSERT INTO users(barcode, first_name, last_name, birthday, email, can_manage_records, can_check_out, creation_date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", data)
                self.parent.db.dbConnection.commit()

                logging.info(f'Created user with barcode {data[0]}')

                self.parent.tab_controller.select(0)
                self.destroy()
        except sqlite3.IntegrityError:
            self.parent.db.unique_conflict()
