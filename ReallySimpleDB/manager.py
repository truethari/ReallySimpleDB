import os
import sqlite3

from .utils     import DATA_TYPES

class ReallySimpleDB:
    def __init__(self) -> None:
        self._add_columns_cmd = ""
        self.connection = ""

    def __create_connection(self, database):
        self.connection = sqlite3.connect(database)

    def create_db(self, dbpath, replace=False):
        if replace:
            if os.path.isfile(os.path.realpath(dbpath)):
                os.remove(os.path.realpath(dbpath))

        if not os.path.isfile(os.path.realpath(dbpath)):
            self.connection = sqlite3.connect(os.path.realpath(dbpath))
            return True

        raise FileExistsError(
            "'{}' file exists. for replace add parameter 'replace=True'".format(dbpath)
            )

    def add_columns(self,
            column_name:str,
            datatype:str="TEXT",
            primary_key:bool=False,
            NOT_NULL:bool=False,
            database:str="",
            table:str=""):
        if datatype.upper() not in DATA_TYPES:
            raise TypeError("datatype not supported, '{}'".format(datatype))

        if database != "":
            if table == "":
                raise TypeError ("add_columns() missing 1 required positional argument: 'table'")

            self.__create_connection(database=database)
            cursor = self.connection.cursor()
            sql_cmd = "ALTER TABLE {} ADD COLUMN {} {}".format(table, column_name, datatype)
            if NOT_NULL:
                sql_cmd += " NOT NULL"
            if primary_key:
                sql_cmd += " PRIMARY KEY"
            cursor.execute(sql_cmd)
            return True

        self._add_columns_cmd += (",{} {}".format(column_name, datatype))

        if primary_key:
            self._add_columns_cmd += " PRIMARY KEY"

        if NOT_NULL:
            self._add_columns_cmd += " NOT NULL"

        return True

    def create_table(self, database:str, table_name:str):
        if self._add_columns_cmd == "":
            raise NotImplementedError("call 'add_columns' function before create table")

        sql_cmd = "CREATE TABLE {} ({})".format(table_name, self._add_columns_cmd[1:])

        self.__create_connection(database)
        self.connection.execute(sql_cmd)
        return True

    def all_tables(self, database:str):
        self.__create_connection(database)
        cursor = self.connection.cursor()
        sql_cmd = "SELECT name FROM sqlite_master WHERE type='table';"
        return [student[0] for student in cursor.execute(sql_cmd)]

    def is_table(self, database:str, table_name:str):
        self.__create_connection(database)
        if table_name in self.all_tables(database):
            return True
        return False

    def delete_table(self, database, table_name):
        pass

    def close_connection(self):
        self.connection.close()
        return True
