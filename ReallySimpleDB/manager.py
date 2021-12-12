import sqlite3

class ReallySimpleDB:
    def __init__(self) -> None:
        pass

    def create_db(self, dbname, replace=False):
        connection = sqlite3.connect(dbname)
        connection.close()