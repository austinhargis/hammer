import os
import random
import sqlite3
from datetime import datetime

from popup_window import PopupWindow


class Database:

    def __init__(self, filename, parent):
        self.parent = parent

        if filename not in os.listdir(f'{self.parent.data_path}'):
            self.dbConnection = sqlite3.connect(f'{self.parent.data_path}/{filename}')
            self.dbCursor = self.dbConnection.cursor()
            self.dbCursor.execute(f"""
                CREATE TABLE item_record(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,     
                    title varchar,
                    author varchar,
                    publish_date varchar,
                    type varchar,
                    location varchar,
                    quantity varchar,
                    description varchar,
                    creation_date datetime,
                    managed_date datetime
                )""")
            self.dbCursor.execute(f"""
                CREATE TABLE locations(
                    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode varchar UNIQUE NOT NULL,
                    name varchar
                )
                """)
            self.dbCursor.execute(f"""
                CREATE TABLE items(
                    id INTEGER,
                    barcode varchar PRIMARY KEY NOT NULL,
                    location_barcode varchar,
                    description varchar,
                    FOREIGN KEY(id) REFERENCES item_record(id),
                    FOREIGN KEY(location_barcode) REFERENCES locations(location_id)
                )
                """)
            self.dbCursor.execute(f"""
                CREATE TABLE users(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode varchar UNIQUE,
                    first_name varchar,
                    last_name varchar,
                    creation_date date,
                    can_check_out integer,
                    can_create_records integer,
                    can_delete_records integer,
                    birthday date,
                    email varchar
                )""")
            self.dbCursor.execute(f"""
                CREATE TABLE checkouts(
                    user_barcode varchar,
                    item_barcode varchar UNIQUE,
                    creation_date datetime,
                    FOREIGN KEY(user_barcode) REFERENCES users(barcode),
                    FOREIGN KEY(item_barcode) REFERENCES items(barcode)
                )""")
            self.dbConnection.commit()

        else:
            self.dbConnection = sqlite3.connect(f'{self.parent.data_path}/{filename}')
            self.dbCursor = self.dbConnection.cursor()

    def delete_query(self, data):
        """
            deletes desired data from the table
            :param data: a tuple of the data that needs to be deleted from the table
            :return: nothing
        """

        item_barcodes = self.dbCursor.execute(f"""
            SELECT barcode
            FROM items
            WHERE id=?
        """, (data[0],)).fetchall()

        checkouts_with_barcode = []
        for barcode in item_barcodes:
            checkouts = self.dbCursor.execute(f"""
                SELECT *
                FROM checkouts
                WHERE item_barcode=?
            """, list(barcode, )).fetchall()
            if len(checkouts) > 0:
                checkouts_with_barcode.append(checkouts[0])

        if len(checkouts_with_barcode) == 0:
            self.dbCursor.execute(f"""DELETE FROM items WHERE id={data[0]}""")
            self.dbCursor.execute(f"""DELETE FROM item_record WHERE id={data[0]}""")
            self.dbConnection.commit()
        else:
            PopupWindow(self.parent,
                        title="Item Currently Checked Out",
                        message="Warning: An item with this barcode is currently checked out, "
                                "you CANNOT delete this barcode at this time.")

    def drop_table(self):
        """
            drops all data from the inventory table
            :return: nothing
        """

        self.dbCursor.execute("""DELETE FROM item_record""")
        self.dbCursor.execute("""DELETE FROM items""")
        self.dbCursor.execute("""DELETE FROM checkouts""")
        self.dbCursor.execute("""DELETE FROM users""")
        self.dbConnection.commit()

    def get_all_query(self):
        """
            allows for receiving all the data in the table
            :return: a list of tuples of data in the table
        """

        self.dbCursor.execute("""SELECT * FROM item_record""")
        return self.dbCursor.fetchall()

    def unique_conflict(self):
        PopupWindow(self.parent,
                    title="Barcode in Use",
                    message="Warning: An item or user already exists with this barcode. "
                            "Please try a different barcode.")
