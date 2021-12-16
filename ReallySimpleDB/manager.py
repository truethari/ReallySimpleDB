import os
import sqlite3

from .utils     import DATA_TYPES

class ReallySimpleDB:
    def __init__(self) -> None:
        self._add_columns_cmd = ""
        self.connection = ""

    def clean(self):
        self._add_columns_cmd = ""

    def create_connection(self, database):
        self.connection = sqlite3.connect(database)

    def create_db(self, dbpath:str="", replace:bool=False):
        if self.connection == "" and not len(dbpath):
            raise TypeError("create_db() missing 1 required positional argument: 'dbpath'")

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
            not_null:bool=False,
            database:str="",
            table:str=""):
        if datatype.upper() not in DATA_TYPES:
            raise TypeError("datatype not supported, '{}'".format(datatype))

        if database != "":
            if table == "":
                raise TypeError("add_columns() missing 1 required positional argument: 'table'")

            self.create_connection(database=database)
            cursor = self.connection.cursor()
            sql_cmd = "ALTER TABLE {} ADD COLUMN {} {}".format(table, column_name, datatype)
            if not_null:
                sql_cmd += " NOT NULL"
            if primary_key:
                sql_cmd += " PRIMARY KEY"
            cursor.execute(sql_cmd)
            return True

        self._add_columns_cmd += (",{} {}".format(column_name, datatype))

        if primary_key:
            self._add_columns_cmd += " PRIMARY KEY"

        if not_null:
            self._add_columns_cmd += " NOT NULL"

        return True

    def create_table(self, table_name:str, database:str=""):
        if self.connection == "" and not len(database):
            raise TypeError("create_table() missing 1 required positional argument: 'database'")

        if len(database):
            self.create_connection(database)

        if self._add_columns_cmd == "":
            raise NotImplementedError("call 'add_columns' function before create table")

        sql_cmd = "CREATE TABLE {} ({})".format(table_name, self._add_columns_cmd[1:])

        self.connection.execute(sql_cmd)
        return True

    def all_tables(self, database:str=""):
        if self.connection == "" and not len(database):
            raise TypeError("all_tables() missing 1 required positional argument: 'database'")

        if len(database):
            self.create_connection(database)

        cursor = self.connection.cursor()
        sql_cmd = "SELECT name FROM sqlite_master WHERE type='table';"
        return [student[0] for student in cursor.execute(sql_cmd)]

    def is_table(self, table_name:str, database:str=""):
        if self.connection == "" and not len(database):
            raise TypeError("is_table() missing 1 required positional argument: 'database'")

        if len(database):
            self.create_connection(database)

        if table_name in self.all_tables(database):
            return True
        return False

    def delete_table(self, table:str, database:str=""):
        if self.connection == "" and not len(database):
            raise TypeError("delete_table() missing 1 required positional argument: 'database'")

        if len(database):
            self.create_connection(database)

        if self.is_table(table_name=table):
            cursor = self.connection.cursor()
            sql_cmd = "DROP TABLE {};".format(table)
            cursor.execute(sql_cmd)
            return True

        return False

    def get_all_column_types(self, table:str, database:str=""):
        if self.connection == "" and not len(database):
            raise TypeError("get_all_column_types() missing 1 required positional argument: 'database'")

        if len(database):
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()
            sql_cmd = "PRAGMA TABLE_INFO({});".format(table)
            fetch = cursor.execute(sql_cmd)

            data_dict = {}
            for data in fetch.fetchall():
                data_dict[data[1]] = data[2]

            return data_dict
        return False

    def get_column_type(self, table:str, column:str, database:str=""):
        all_data = self.get_all_column_types(table=table, database=database)
        if type(all_data) != bool and column in all_data:
            return all_data[column]
        return False

    def close_connection(self):
        self.connection.close()
        return True
