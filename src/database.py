import bcrypt
from dotenv import load_dotenv
import mysql.connector
import os
import threading

from popup_window import PopupWindow


class Database(threading.Thread):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        load_dotenv()

        self.dbConnection = mysql.connector.connect(
            host=os.getenv('db_host'),
            user=os.getenv('db_user'),
            password=os.getenv('db_password'),
            autocommit=True,
        )
        self.dbCursor = self.dbConnection.cursor(buffered=True)
        try:
            self.dbCursor.execute("""
                CREATE DATABASE hammerDB;
            """)
            self.dbCursor.execute("""
                USE hammerDB;
            """)
            self.dbCursor.execute(f"""
                CREATE TABLE item_record(
                    id smallint(255) NOT NULL AUTO_INCREMENT,     
                    title varchar(255),
                    author varchar(255),
                    publish_date varchar(255),
                    type varchar(255),
                    location varchar(255),
                    quantity varchar(255),
                    description varchar(255),
                    creation_date datetime,
                    managed_date datetime,
                    PRIMARY KEY (id)
                )""")
            self.dbCursor.execute(f"""
                CREATE TABLE locations(
                    location_id smallint(255) AUTO_INCREMENT,
                    barcode varchar(255) UNIQUE NOT NULL,
                    name varchar(255),
                    PRIMARY KEY (location_id)
                )
                """)
            self.dbCursor.execute(f"""
                CREATE TABLE items(
                    id smallint(255),
                    barcode varchar(255) NOT NULL,
                    location_barcode varchar(255),
                    description varchar(255),
                    PRIMARY KEY (barcode),
                    FOREIGN KEY(id) REFERENCES item_record(id),
                    FOREIGN KEY(location_barcode) REFERENCES locations(barcode)
                )
                """)
            self.dbCursor.execute(f"""
                CREATE TABLE users(
                    user_id smallint(255) AUTO_INCREMENT,
                    barcode varchar(255) UNIQUE,
                    first_name varchar(255),
                    last_name varchar(255),
                    password varchar(255),
                    creation_date date,
                    can_check_out boolean,
                    can_manage_records boolean,
                    can_modify_users boolean,
                    is_admin boolean,
                    birthday date,
                    email varchar(255),
                    PRIMARY KEY (user_id)
                )""")
            self.dbCursor.execute(f"""
                CREATE TABLE checkouts(
                    user_barcode varchar(255),
                    item_barcode varchar(255) UNIQUE,
                    creation_date datetime,
                    FOREIGN KEY(user_barcode) REFERENCES users(barcode),
                    FOREIGN KEY(item_barcode) REFERENCES items(barcode)
                )""")
            self.dbCursor.execute("""
                INSERT INTO users (barcode, first_name, last_name, password, birthday, email, is_admin, can_check_out, can_manage_records, can_modify_users)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ('admin', 'admin', 'admin', bcrypt.hashpw('12345'.encode('utf-8'), bcrypt.gensalt()), '2023-02-01', '', 1, 1, 1, 1))
        except mysql.connector.errors.DatabaseError:
            self.dbCursor.execute("""
                USE hammerDB;
            """)

    def delete_query(self, data):
        """
            deletes desired data from the table
            :param data: a tuple of the data that needs to be deleted from the table
            :return: nothing
        """

        self.dbCursor.execute(f"""
            SELECT barcode
            FROM items
            WHERE id=%s
        """, (data[0],))
        item_barcodes = self.dbCursor.fetchall()

        checkouts_with_barcode = []
        for barcode in item_barcodes:
            self.dbCursor.execute(f"""
                SELECT *
                FROM checkouts
                WHERE item_barcode=%s
            """, list(barcode, ))
            checkouts = self.dbCursor.fetchall()
            if len(checkouts) > 0:
                checkouts_with_barcode.append(checkouts[0])

        if len(checkouts_with_barcode) == 0:
            self.dbCursor.execute(f"""DELETE FROM items WHERE id={data[0]}""")
            self.dbCursor.execute(f"""DELETE FROM item_record WHERE id={data[0]}""")
            self.dbConnection.commit()
        else:
            PopupWindow(self.parent,
                        title=self.parent.get_region_text('item_cant_delete_error_title'),
                        message=self.parent.get_region_text('item_cant_delete_error_body'))

    def get_all_query(self):
        """
            allows for receiving all the data in the table
            :return: a list of tuples of data in the table
        """

        self.dbCursor.execute("""SELECT * FROM item_record""")
        return self.dbCursor.fetchall()

    def unique_conflict(self):
        PopupWindow(self.parent,
                    title=self.parent.get_region_text('item_barcode_in_use_error_title'),
                    message=self.parent.get_region_text('item_barcode_in_use_error_body'))
