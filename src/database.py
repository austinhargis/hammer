import sqlite3
import os
import random
import tkinter as tk
from datetime import datetime
from tkinter import ttk


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
                CREATE TABLE items(
                    id INTEGER,
                    barcode varchar PRIMARY KEY,
                    location varchar,
                    FOREIGN KEY(id) REFERENCES item_record(id)
                )
            """)
            self.dbCursor.execute(f"""
                    CREATE TABLE users(
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        barcode varchar UNIQUE,
                        first_name varchar,
                        last_name varchar,
                        creation_date date
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

    def insert_query(self, item_information, item):
        """
            inserts data into the inventory table
            :param item_information:
            :param item: a tuple of data to be inserted into the table
            :return: nothing
        """
        if item_information[0].replace(' ', '') == '' or item[0].replace(' ', '') == '':
            popup = tk.Toplevel(padx=self.parent.padding, pady=self.parent.padding)
            popup.attributes('-topmost', True)
            popup.title("Error!")
            ttk.Label(popup,
                      text="The barcode and title field must have a value"
                           "specified before they can be added to the table.",
                      wraplength=self.parent.wraplength,
                      justify='center').pack()
            ttk.Button(popup, text="Continue", command=popup.destroy).pack()

            popup.mainloop()

            return

        try:
            item_information = list(item_information)
            item_information.append(datetime.now())
            item_information.append(datetime.now())
            self.dbCursor.execute(f"""INSERT INTO item_record(title, author, description, publish_date, type, creation_date, managed_date)
                                      VALUES (?, ?, ?, ?, ?, ?, ?)""", item_information)
            self.dbConnection.commit()
        except sqlite3.IntegrityError:
            self.unique_conflict()

    def delete_query(self, data):
        """
            deletes desired data from the table
            :param data: a tuple of the data that needs to be deleted from the table
            :return: nothing
        """
        print(data)
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
            """, list(barcode,)).fetchall()
            if len(checkouts) > 0:
                checkouts_with_barcode.append(checkouts[0])

        if len(checkouts_with_barcode) == 0:
            self.dbCursor.execute(f"""DELETE FROM items WHERE id={data[0]}""")
            self.dbCursor.execute(f"""DELETE FROM item_record WHERE id={data[0]}""")
            self.dbConnection.commit()
        else:
            popup = tk.Toplevel(padx=self.parent.padding, pady=self.parent.padding)
            popup.title('Barcode Currently Checked Out')

            ttk.Label(popup,
                      text='Warning: An item with this barcode is currently checked out, '
                           'you CANNOT delete the barcode at this time.',
                      wraplength=self.parent.wraplength,
                      justify='center').pack()
            ttk.Button(popup, text='Continue', command=lambda: popup.destroy()).pack()

            popup.mainloop()

    def test_add_query(self):
        """
            a query for adding test data to the database
            :return: nothing
        """

        data = ["Test1", "Test2", "Test3", "Test4", "Test5", datetime.now(), datetime.now()]
        self.dbCursor.execute(f"""INSERT INTO item_record (title, author, description, publish_date, type, creation_date, managed_date)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)""", data)
        self.dbConnection.commit()

    def test_add_item_query(self):
        selected = self.parent.tree.item(self.parent.tree.focus())
        record_id = selected['values'][0]

        data = (record_id, f"Test{random.randint(0,1000)}", "Test")

        self.dbCursor.execute(f"""
            INSERT INTO items (id, barcode, location) 
            VALUES (?, ?, ?)
        """, data)
        self.dbConnection.commit()

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

    def update_query(self, data, row_id):
        """
            allows for the updating of an entry into hammer's database
            :param data a tuple of all the data for the row
            :param row_id the ID for the row being updated
            :return nothing
        """

        try:
            data = list(data)
            data.append(datetime.now())
            self.dbCursor.execute(f"""UPDATE item_record 
                                      SET title=?, author=?, description=?, publish_date=?, type=?, managed_date=?
                                      WHERE id={row_id}""", data)

            self.dbConnection.commit()
        except sqlite3.IntegrityError:
            self.unique_conflict()

    def get_all_query(self):
        """
            allows for receiving all the data in the table
            :return: a list of tuples of data in the table
        """

        self.dbCursor.execute("""SELECT * FROM item_record""")
        return self.dbCursor.fetchall()

    def unique_conflict(self):
        popup = tk.Toplevel(padx=self.parent.padding, pady=self.parent.padding)
        popup.title('Barcode In Use')

        ttk.Label(popup,
                  text='Warning: An item or user already exists with this barcode.'
                       'Please try a different barcode.',
                  wraplength=self.parent.wraplength,
                  justify='center').pack()
        ttk.Button(popup, text='Continue', command=lambda: popup.destroy()).pack()

        popup.mainloop()

    def cant_change_error(self):
        popup = tk.Toplevel(padx=self.parent.padding, pady=self.parent.padding)
        popup.title('Barcode Currently Checked Out')

        ttk.Label(popup,
                  text='Warning: An item with this barcode is currently checked out, '
                       'you CANNOT change the barcode at this time.',
                  wraplength=self.parent.wraplength,
                  justify='center').pack()
        ttk.Button(popup, text='Continue', command=lambda: popup.destroy()).pack()

        popup.mainloop()
