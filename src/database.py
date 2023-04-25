import os
import random
import sqlite3
import mysql.connector
from datetime import datetime

from popup_window import PopupWindow


class Database:

    def __init__(self, filename, parent):
        self.parent = parent

        # if filename not in os.listdir(f'{self.parent.data_path}'):
        self.dbConnection = mysql.connector.connect(
            host='',
            user='',
            password=''
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
                    creation_date date,
                    can_check_out boolean,
                    can_manage_records boolean,
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
        except mysql.connector.errors.DatabaseError:
            self.dbCursor.execute("""
                USE hammerDB;
            """)
            # self.dbConnection.commit()

        # else:
        #     self.dbConnection = sqlite3.connect(f'{self.parent.data_path}/{filename}')
        #     self.dbCursor = self.dbConnection.cursor()

    def delete_query(self, data):
        """
            deletes desired data from the table
            :param data: a tuple of the data that needs to be deleted from the table
            :return: nothing
        """

        item_barcodes = self.dbCursor.execute(f"""
            SELECT barcode
            FROM items
            WHERE id=%s
        """, (data[0],)).fetchall()

        checkouts_with_barcode = []
        for barcode in item_barcodes:
            checkouts = self.dbCursor.execute(f"""
                SELECT *
                FROM checkouts
                WHERE item_barcode=%s
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
