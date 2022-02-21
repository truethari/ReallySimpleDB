import os
import sqlite3

from .utils     import DATA_TYPES

class ReallySimpleDB:
    def __init__(self) -> None:
        self._add_columns_cmd = ""
        self.connection = ""

    def _not_table(self, table:str):
        raise sqlite3.OperationalError("no such table: {}".format(table))

    def clean(self):
        self._add_columns_cmd = ""

    def create_connection(self, database):
        self.connection = sqlite3.connect(database)

    def create_db(self, dbpath:str="", replace:bool=False):
        if self.connection == "" and not dbpath:
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
        if self.connection == "" and not database:
            raise TypeError("create_table() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self._add_columns_cmd == "":
            raise NotImplementedError("call 'add_columns' function before create table")

        sql_cmd = "CREATE TABLE {} ({})".format(table_name, self._add_columns_cmd[1:])

        self.connection.execute(sql_cmd)
        return True

    def all_tables(self, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("all_tables() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        cursor = self.connection.cursor()
        sql_cmd = "SELECT name FROM sqlite_master WHERE type='table';"
        return [student[0] for student in cursor.execute(sql_cmd)]

    def is_table(self, table_name:str, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("is_table() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if table_name in self.all_tables(database):
            return True
        return False

    def delete_table(self, table:str, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("delete_table() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table):
            cursor = self.connection.cursor()
            sql_cmd = "DROP TABLE {};".format(table)
            cursor.execute(sql_cmd)

            return True

        self._not_table(table=table)

    def get_all_column_types(self, table:str, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("get_all_column_types() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            sql_cmd = "PRAGMA TABLE_INFO({});".format(table)
            fetch = cursor.execute(sql_cmd)

            data_dict = {}
            for data in fetch.fetchall():
                data_dict[data[1]] = data[2]

            return data_dict

        self._not_table(table=table)

    def get_column_type(self, table:str, column:str, database:str=""):
        all_data = self.get_all_column_types(table=table, database=database)
        if (not isinstance(all_data, bool)) and (column in all_data):
            return all_data[column]
        return False

    def get_columns(self, table:str, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("get_columns() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        column_types = self.get_all_column_types(table=table, database=database)
        columns = []
        if isinstance(column_types, dict):
            for column in column_types:
                columns.append(column)

        return columns

    def get_primary_key(self, table:str, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("get_primary_key() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            sql_cmd = "SELECT * FROM pragma_table_info('{}') WHERE pk;".format(table)
            fetch = cursor.execute(sql_cmd)

            return fetch.fetchall()[0][1]

        self._not_table(table=table)

    def add_record(self, table:str, record, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("add_record() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            tmp_all_columns = self.get_all_column_types(table=table, database=database)
            all_columns = {}
            for column in tmp_all_columns:
                all_columns[column] = ""

            fields = []
            sql_cmd = "INSERT INTO {} VALUES(".format(table)
            if isinstance(record, dict):
                for field in record:
                    if field not in all_columns:
                        raise NameError("'{}' column is not in the table".format(field))

                    if DATA_TYPES[tmp_all_columns[field]] == type(record[field]):
                        all_columns[field] = record[field]
                    else:
                        raise TypeError("The '{}' field requires the '{}' type but got the '{}' type".format(field, DATA_TYPES[tmp_all_columns[field]], type(record[field])))

                for field in all_columns:
                    fields.append(all_columns[field])
                    sql_cmd+= "?,"

                sql_cmd = sql_cmd[:-1] + ");"

                cursor.execute(sql_cmd, fields)
                self.connection.commit()
            else:
                raise TypeError("'record' must be dict")

            return True

        self._not_table(table=table)

    def get_record(self, table:str, primary_key, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("get_record() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            sql_cmd = "SELECT * FROM {} WHERE {}=?;".format(table, self.get_primary_key(table=table, database=database))
            fetch = cursor.execute(sql_cmd, (primary_key,))

            columns = self.get_columns(table=table, database=database)
            record = {}

            try:
                for index, data in enumerate(fetch.fetchall()[0]):
                    record[columns[index]] = data
            except IndexError:
                return {}

            return record

        self._not_table(table=table)

    def get_all_records(self, table:str, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("get_all_records() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            sql_cmd = "SELECT * FROM {}".format(table)
            cursor.execute(sql_cmd)
            rows = cursor.fetchall()

            columns = self.get_columns(table=table, database=database)
            records = []
            tmp_dict = {}

            for row in rows:
                for index, data in enumerate(row):
                    tmp_dict[columns[index]] = data
                records.append(tmp_dict)
                tmp_dict = {}

            return records

        self._not_table(table=table)

    def delete_record(self, table:str, primary_key, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("delete_record() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()
            sql = "DELETE FROM {} WHERE {}=?".format(table, self.get_primary_key(table=table, database=database))
            cursor.execute(sql, (primary_key,))
            self.connection.commit()

            return True

        self._not_table(table=table)

    def filter_records(self, table:str, values:dict, database:str=""):
        if self.connection == "" and not database:
            raise TypeError("filter_records() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            sql = "SELECT * FROM {} WHERE ".format(table)

            for value in values:
                try:
                    sql += value + "='" + values[value] + "' AND "
                except TypeError:
                    sql += value + "=" + str(values[value]) + " AND "

            sql = sql[:-5] + ";"

            cursor.execute(sql)
            rows = cursor.fetchall()

            columns = self.get_columns(table=table, database=database)
            records = []
            tmp_dict = {}

            for row in rows:
                for index, data in enumerate(row):
                    tmp_dict[columns[index]] = data
                records.append(tmp_dict)
                tmp_dict = {}

            return records

        self._not_table(table=table)

    def close_connection(self):
        self.connection.close()
        return True
