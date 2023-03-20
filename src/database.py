import sqlite3
import os
import random


class Database:

    def __init__(self, filename):
        if filename not in os.listdir():
            self.dbConnection = sqlite3.connect(filename)
            self.dbCursor = self.dbConnection.cursor()
            self.dbCursor.execute(f"CREATE TABLE inventory("
                                  f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                  f"title varchar, "
                                  f"author varchar, "
                                  f"publish_date varchar, "
                                  f"type varchar, "
                                  f"location varchar, "
                                  f"quantity varchar)")
            self.dbConnection.commit()

        else:
            self.dbConnection = sqlite3.connect(filename)
            self.dbCursor = self.dbConnection.cursor()

    def insert_query(self, data):
        self.dbCursor.execute(f"INSERT INTO inventory(title, author, publish_date, type, location, quantity)"
                              f"VALUES (?, ?, ?, ?, ?, ?)", data)
        self.dbConnection.commit()

    def delete_query(self, data):
        print(data)
        print(data[0])

        self.dbCursor.execute(f"DELETE FROM inventory WHERE id={data[0]}")
        self.dbConnection.commit()

    # Currently adds filler data to the table
    def test_add_query(self):
        data = ["Test", "Test2", "Test3", "Test4", "Test5", "Test6"]
        self.dbCursor.execute(f"INSERT INTO inventory (title, author, publish_date, type, location, quantity)"
                              f"VALUES (?, ?, ?, ?, ?, ?)", data)
        self.dbConnection.commit()

    # Currently drops all data from the inventory table
    def drop_table(self):
        self.dbCursor.execute("DELETE FROM inventory")
        self.dbConnection.commit()

    # TODO: implement update query
    def update_query(self):
        pass

    # Returns all rows in the inventory table
    def get_all_query(self):
        self.dbCursor.execute("SELECT * FROM inventory")
        return self.dbCursor.fetchall()
