import os
import sqlite3

class ReallySimpleDB:
    def __init__(self) -> None:
        pass

    def create_db(self, dbpath, replace=False):
        if replace or not os.path.isfile(os.path.realpath(dbpath)):
            self.connection = sqlite3.connect(dbpath)
            return True

        else:
            raise FileExistsError("'{}' file exists. for replace add parameter 'replace=True'".format(dbpath))

    def close_connection(self):
        self.connection.close()
        return True
