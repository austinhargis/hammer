import sqlite3
import tkinter as tk
from tkinter import ttk

from record_child_template import RecordChildTemplate


class AddItemFromRecordWindow(RecordChildTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.heading_label.configure(text='Create Item From Record')

        ttk.Button(self.button_frame, text='Add Item to Record', command=lambda: self.create_item()).pack(side='left')

    def create_item(self):
        try:
            self.parent.db.dbCursor.execute("""
                INSERT INTO items
                VALUES (?, ?, ?)
            """, self.get_item_info())
            self.parent.db.dbConnection.commit()
            self.destroy()
        except sqlite3.IntegrityError:
            self.parent.db.unique_conflict()
