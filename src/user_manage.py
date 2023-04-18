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

        self.email_entry.bind('<Return>', lambda event: self.manage_user())

        self.load_user()

        self.barcode_entry.configure(state='disabled')
        self.first_name_entry.focus()

    def load_user(self):
        user_data = self.parent.db.dbCursor.execute(f"""
            SELECT user_id, barcode, first_name, last_name, birthday, email, can_manage_records, can_check_out FROM users
            WHERE barcode=?
        """, (self.barcode,)).fetchall()

        self.user_id = user_data[0][0]
        self.barcode_entry.insert('', user_data[0][1])
        self.first_name_entry.insert('', user_data[0][2])
        self.last_name_entry.insert('', user_data[0][3])
        self.birthday_entry.insert('', user_data[0][4])
        self.email_entry.insert('', user_data[0][5])
        self.manage_item_value.set(user_data[0][6])
        self.check_out_value.set(user_data[0][7])

    def manage_user(self):
        try:
            if self.get_all_data()[0][0:1] == 'U':
                self.parent.db.dbCursor.execute(f"""
                    UPDATE users
                    SET barcode=?, first_name=?, last_name=?, birthday=?, email=?, can_manage_records=?, can_check_out=?
                    WHERE user_id={self.user_id}
                """, self.get_all_data())
                self.parent.db.dbConnection.commit()

                self.destroy()

        except sqlite3.IntegrityError:
            pass
