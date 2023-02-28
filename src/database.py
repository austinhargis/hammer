import sqlite3
import os


class Database:

    def __init__(self, filename):
        if filename not in os.listdir():
            self.dbConnection = sqlite3.connect(filename)
            self.dbCursor = self.dbConnection.cursor()
            self.dbCursor.execute(f"CREATE TABLE inventory(id integer primary key, "
                                  "title varchar, "
                                  "author varchar, "
                                  "publish_date varchar, "
                                  "type varchar, "
                                  "location varchar, "
                                  "quantity varchar)")
            pass

        else:
            self.dbConnection = sqlite3.connect(filename)
            self.dbCursor = self.dbConnection.cursor()

    # TODO: implement add query 
    def add_query(self):
        pass

    # TODO: implement delete query
    def delete_query(self):
        pass

    # TODO: implement update query
    def update_query(self):
        pass
