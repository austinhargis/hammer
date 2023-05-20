import logging
import mysql.connector
from datetime import datetime
from user_template import UserTemplate


class CreateUser(UserTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title_label.configure(text=self.parent.get_region_text('user_create_heading'))

        self.confirm_button.configure(
            text=self.parent.get_region_text('user_create_heading'),
            command=lambda: self.add_user())

        self.manage_item_check.bind('<Return>', lambda event: self.add_user())

    def add_user(self):
        try:
            data = self.get_all_data()
            data.append(datetime.now())

            self.parent.db.dbCursor.execute(f"""
                INSERT INTO users(barcode, first_name, last_name, password, birthday, email, is_admin, can_manage_records, can_check_out, can_modify_users, creation_date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data)
            self.parent.db.dbConnection.commit()

            logging.info(f'Created user with barcode {data[0]}')
            self.parent.tab_controller.select(0)
            self.destroy()
        except mysql.connector.errors.IntegrityError:
            self.parent.db.unique_conflict()
