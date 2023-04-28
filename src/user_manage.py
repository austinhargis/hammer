from user_template import UserTemplate


class ManageUser(UserTemplate):

    def __init__(self, parent, barcode):
        super().__init__(parent)

        self.parent = parent
        self.barcode = barcode

        self.title_label.configure(text=self.parent.get_region_text('user_manage'))

        self.confirm_button.configure(
            text=self.parent.get_region_text('user_manage_save'),
            command=lambda: self.manage_user())

        self.manage_item_check.bind('<Return>', lambda event: self.manage_user())

        self.load_user()

        self.barcode_entry.configure(state='disabled')
        self.first_name_entry.focus()

    def load_user(self):
        self.parent.db.dbCursor.execute(f"""
            SELECT user_id, barcode, first_name, last_name, birthday, email, is_admin, can_manage_records, can_check_out, can_modify_users FROM users
            WHERE barcode=%s
        """, (self.barcode,))
        user_data = self.parent.db.dbCursor.fetchall()

        self.user_id = user_data[0][0]
        self.barcode_entry.insert('', user_data[0][1])
        self.first_name_entry.insert('', user_data[0][2])
        self.last_name_entry.insert('', user_data[0][3])
        self.birthday_calendar.selection_set(user_data[0][4])
        self.email_entry.insert('', user_data[0][5])
        self.is_admin_value.set(user_data[0][6])
        self.manage_item_value.set(user_data[0][7])
        self.check_out_value.set(user_data[0][8])
        self.can_modify_users.set(user_data[0][9])

    def manage_user(self):
        if self.password_entry.get() != '':
            self.parent.db.dbCursor.execute(f"""
                UPDATE users
                SET barcode=%s, first_name=%s, last_name=%s, password=%s, birthday=%s, email=%s, is_admin=%s, can_manage_records=%s, can_check_out=%s, can_modify_users=%s
                WHERE user_id={self.user_id}
            """, self.get_all_data())
        else:
            data = self.get_all_data()
            del data[3]
            self.parent.db.dbCursor.execute(f"""
                            UPDATE users
                            SET barcode=%s, first_name=%s, last_name=%s, birthday=%s, email=%s, is_admin=%s, can_manage_records=%s, can_check_out=%s, can_modify_users=%s
                            WHERE user_id={self.user_id}
            """, data)
        self.parent.db.dbConnection.commit()
        self.parent.get_user_permissions()
        self.destroy()
