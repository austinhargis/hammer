import sqlite3


class Database:
    
    def __init__(self, filename):
        self.dbConnection = sqlite3.connect(filename)
        self.dbCursor = self.dbConnection.cursor()

        # TODO: implement add query 
    def addQuery(self):
        pass

    # TODO: implement delete query
    def deleteQuery(self):
        pass

    # TODO: implement update query
    def updateQuery(self):
        pass

