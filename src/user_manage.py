import sqlite3

from languages import *
from user_template import UserTemplate


class ManageUser(UserTemplate):

    def __init__(self, parent, barcode):
        super().__init__(parent)

        self.parent = parent
        self.barcode = barcode

        self.title_label.configure(text='Manage User')

        self.confirm_button.configure(
            text='Save User',
            command=lambda: self.manage_user())

        self.last_name_entry.bind('<Return>', lambda event: self.manage_user())

        self.load_user()

    def load_user(self):
        print(self.barcode)
        user_data = self.parent.db.dbCursor.execute(f"""
            SELECT user_id, barcode, first_name, last_name FROM users
            WHERE barcode=?
        """, (self.barcode,)).fetchall()

        self.user_id = user_data[0][0]
        self.barcode_entry.insert('', user_data[0][1])
        self.first_name_entry.insert('', user_data[0][2])
        self.last_name_entry.insert('', user_data[0][3])

    def manage_user(self):

        try:
            if self.get_all_data()[0][0:1] == 'U':
                self.parent.db.dbCursor.execute(f"""
                    UPDATE users
                    SET barcode=?, first_name=?, last_name=?
                    WHERE user_id={self.user_id}
                """, self.get_all_data())
                self.parent.db.dbConnection.commit()

        except sqlite3.IntegrityError:
            pass
