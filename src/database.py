import sqlite3
import os
import random
import tkinter as tk
from tkinter import ttk


class Database:

    def __init__(self, filename):
        if filename not in os.listdir():
            self.dbConnection = sqlite3.connect(filename)
            self.dbCursor = self.dbConnection.cursor()
            self.dbCursor.execute(f"""
                    CREATE TABLE inventory(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        barcode varchar,
                        title varchar,
                        author varchar,
                        publish_date varchar,
                        type varchar,
                        location varchar,
                        quantity varchar
                    )""")
            self.dbConnection.commit()

        else:
            self.dbConnection = sqlite3.connect(filename)
            self.dbCursor = self.dbConnection.cursor()

    def insert_query(self, data):
        """
            inserts data into the inventory table
            :param data: a tuple of data to be inserted into the table
            :return: nothing
        """

        if data[1].replace(' ', '') == '':
            popup = tk.Toplevel()
            popup.title("Error!")
            tk.Label(popup, text="The title field must have a value specified.").grid(row=0, column=0)
            ttk.Button(popup, text="Okay", command=popup.destroy).grid(row=1, column=0)

            return

        self.dbCursor.execute(f"""INSERT INTO inventory(barcode, title, author, publish_date, type, location, quantity)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)""", data)
        self.dbConnection.commit()

    def delete_query(self, data):
        """
            deletes desired data from the table
            :param data: a tuple of the data that needs to be deleted from the table
            :return: nothing
        """

        self.dbCursor.execute(f"""DELETE FROM inventory WHERE id={data[0]}""")
        self.dbConnection.commit()

    def test_add_query(self):
        """
            a query for adding test data to the database
            :return: nothing
        """

        data = ["Test", "Test1", "Test2", "Test3", "Test4", "Test5", "Test6"]
        self.dbCursor.execute(f"""INSERT INTO inventory (barcode, title, author, publish_date, type, location, quantity)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)""", data)
        self.dbConnection.commit()

    def drop_table(self):
        """
            drops all data from the inventory table
            :return: nothing
        """

        self.dbCursor.execute("""DELETE FROM inventory""")
        self.dbConnection.commit()

    def update_query(self, data, row_id):
        """
            allows for the updating of an entry into hammer's database
            :param data a tuple of all the data for the row
            :param row_id the ID for the row being updated
            :return nothing
        """

        self.dbCursor.execute(f"""UPDATE inventory 
                                  SET title=?, author=?, publish_date=?, type=?,
                                  location=?, quantity=?
                                  WHERE id={row_id}""", data)
        self.dbConnection.commit()

    def get_all_query(self):
        """
            allows for receiving all the data in the table
            :return: a list of tuples of data in the table
        """

        self.dbCursor.execute("""SELECT * FROM inventory""")
        return self.dbCursor.fetchall()
