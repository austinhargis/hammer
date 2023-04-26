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

        self.manage_item_check.bind('<Return>', lambda event: self.manage_user())

        self.load_user()

        self.barcode_entry.configure(state='disabled')
        self.first_name_entry.focus()

    def load_user(self):
        self.parent.db.dbCursor.execute(f"""
            SELECT user_id, barcode, first_name, last_name, birthday, email, can_manage_records, can_check_out FROM users
            WHERE barcode=%s
        """, (self.barcode,))
        user_data = self.parent.db.dbCursor.fetchall()

        self.user_id = user_data[0][0]
        self.barcode_entry.insert('', user_data[0][1])
        self.first_name_entry.insert('', user_data[0][2])
        self.last_name_entry.insert('', user_data[0][3])
        self.birthday_calendar.selection_set(user_data[0][4])
        self.email_entry.insert('', user_data[0][5])
        self.manage_item_value.set(user_data[0][6])
        self.check_out_value.set(user_data[0][7])

    def manage_user(self):
        data = self.get_all_data()
        del data[3]
        self.parent.db.dbCursor.execute(f"""
            UPDATE users
            SET barcode=%s, first_name=%s, last_name=%s, birthday=%s, email=%s, can_manage_records=%s, can_check_out=%s
            WHERE user_id={self.user_id}
        """, data)
        self.parent.db.dbConnection.commit()

        self.destroy()

        print('sucess?')
