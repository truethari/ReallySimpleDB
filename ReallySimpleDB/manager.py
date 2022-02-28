import os
import sqlite3

from .utils     import DATA_TYPES

class ReallySimpleDB:
    """
    ReallySimpleDB class.

    ReallySimpleDB objects are the ones responsible of creating DBs, connecting
    with them, creating tables, adding records, geting records, among tasks. In
    more cases these should be one per database.
    """

    def __init__(self) -> None:
        """Create a object."""
        self._add_columns_cmd = ""
        self.connection = ""

    def clean(self):
        """
        Clean add_columns data.

        Why? _add_columns_cmd variable is for define SQL command. when using add_column,
        it sets up a string here. but when it is finished this is not clean and the data
        continues to exist. when use add_column again and again, it will be processed
        along with the existing data. this should be used to prevent it.
        """
        self._add_columns_cmd = ""

    def create_connection(self, database):
        """Open a connection to the SQLite database file."""
        self.connection = sqlite3.connect(database)
        return True

    def create_db(self, dbpath:str="", replace:bool=False):
        """Create a new database in a given path."""
        if self.connection == "" and not dbpath:
            raise TypeError("create_db() missing 1 required positional argument: 'dbpath'")

        if replace:
            # delete if database exists in given path
            if os.path.isfile(os.path.realpath(dbpath)):
                os.remove(os.path.realpath(dbpath))

        if not os.path.isfile(os.path.realpath(dbpath)):
            # create new connection with creating new database
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
        """
        Add columns to an existing table / define columns before creating a table.

        If use for create new table: sqlite cannot create table without columns.
        so user must first define the columns and create a table.
        important: user have to close connection here. if not, code returns error.
        because it tries to add column to existing table.
        """
        # checks if the user is trying to add unsupported data type
        if datatype.upper() not in DATA_TYPES:
            raise TypeError("datatype not supported, '{}'".format(datatype))

        if database != "":
            if table == "":
                raise TypeError("add_columns() missing 1 required positional argument: 'table'")

            # if the table is defined, it means that the user is trying to add a
            # column to an existing table.
            self.create_connection(database=database)
            cursor = self.connection.cursor()
            sql_cmd = "ALTER TABLE " + table + " ADD COLUMN " + column_name + " " + datatype
            if not_null:
                sql_cmd += " NOT NULL"
            if primary_key:
                sql_cmd += " PRIMARY KEY"
            cursor.execute(sql_cmd)
            return True

        # if table is not defines, it means that the user is trying to add / define
        # a column to a new table. so the following code add SQL syntax globally for
        # use when creating new table
        self._add_columns_cmd += "," + column_name + " " + datatype

        if primary_key:
            self._add_columns_cmd += " PRIMARY KEY"

        if not_null:
            self._add_columns_cmd += " NOT NULL"

        return True

    def create_table(self, table_name:str, database:str=""):
        """Create new table in database."""
        if self.connection == "" and not database:
            raise TypeError("create_table() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        # if use for create new table: sqlite cannot create table without columns.
        # so user must first define the columns and create a table. using add_columns
        # can define columns for new table.
        if self._add_columns_cmd == "":
            raise NotImplementedError("call 'add_columns' function before create table")

        sql_cmd = "CREATE TABLE " + table_name + " (" + self._add_columns_cmd[1:] + ")"

        self.connection.execute(sql_cmd)
        return True

    def all_tables(self, database:str=""):
        """Get a list of all the tables in the database."""
        if self.connection == "" and not database:
            raise TypeError("all_tables() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        cursor = self.connection.cursor()
        sql_cmd = "SELECT name FROM sqlite_master WHERE type='table';"
        return [tables[0] for tables in cursor.execute(sql_cmd)]

    def is_table(self, table_name:str, database:str=""):
        """Check if the given table is exists in the database."""
        if self.connection == "" and not database:
            raise TypeError("is_table() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if table_name in self.all_tables(database):
            return True
        return False

    def delete_table(self, table:str, database:str=""):
        """Delete a table from the database."""
        if self.connection == "" and not database:
            raise TypeError("delete_table() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table):
            cursor = self.connection.cursor()
            sql_cmd = "DROP TABLE " + table + ";"
            cursor.execute(sql_cmd)

            return True

        # raise OperationalError if the given table not exists
        raise sqlite3.OperationalError("no such table: {}".format(table))

    def get_all_column_types(self, table:str, database:str=""):
        """Get all the column names with the data types in a table."""
        if self.connection == "" and not database:
            raise TypeError(
                "get_all_column_types() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            sql_cmd = "PRAGMA TABLE_INFO(" + table + ");"
            fetch = cursor.execute(sql_cmd)

            data_dict = {}
            for data in fetch.fetchall():
                data_dict[data[1]] = data[2]

            return data_dict

        # raise OperationalError if the given table not exists
        raise sqlite3.OperationalError("no such table: {}".format(table))

    def get_column_type(self, table:str, column:str, database:str=""):
        """Get data type of a column in a table."""
        all_data = self.get_all_column_types(table=table, database=database)

        # if columns exists in the table and given column in the table
        if (not isinstance(all_data, bool)) and (column in all_data):
            return all_data[column]

        raise sqlite3.OperationalError("no such column: {}".format(column))

    def get_columns(self, table:str, database:str=""):
        """Get all the column names list in a table."""
        if self.connection == "" and not database:
            raise TypeError("get_columns() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        # get all columns with data types using get_all_column_types
        column_types = self.get_all_column_types(table=table, database=database)
        columns = []
        if isinstance(column_types, dict):
            for column in column_types:
                columns.append(column)

        return columns

    def get_primary_key(self, table:str, database:str=""):
        """Find and get primary key of a table."""
        if self.connection == "" and not database:
            raise TypeError("get_primary_key() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            sql_cmd = "SELECT * FROM pragma_table_info(?) WHERE pk;"
            fetch = cursor.execute(sql_cmd, (table,))
            return fetch.fetchall()[0][1]

        # raise OperationalError if the given table not exists
        raise sqlite3.OperationalError("no such table: {}".format(table))

    def add_record(self, table:str, record, database:str=""):
        """Add a new record to a table."""
        if self.connection == "" and not database:
            raise TypeError("add_record() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            # get all columns with data types using get_all_column_types
            tmp_all_columns = self.get_all_column_types(table=table, database=database)
            all_columns = {}

            # appends column names of the given table to all_columns dictionary
            for column in tmp_all_columns:
                all_columns[column] = ""

            fields = []
            sql_cmd = "INSERT INTO " + table + " VALUES("

            # if record is dict type,..
            if isinstance(record, dict):
                for field in record:
                    # if the user has defined a column that is not in the table..
                    if field not in all_columns:
                        raise NameError("'{}' column is not in the table".format(field))

                    # if the user has defines values that is match with the
                    # datatypes of the columns..
                    if DATA_TYPES[tmp_all_columns[field]] == type(record[field]):
                        all_columns[field] = record[field]
                    else:
                        raise TypeError("The '{}' field requires '{}' but got '{}'"
                        .format(field, DATA_TYPES[tmp_all_columns[field]], type(record[field])))

                # creates the full SQL command
                for field in all_columns:
                    fields.append(all_columns[field])
                    sql_cmd+= "?,"

                # removes unnecessary characters and complete the SQL command
                sql_cmd = sql_cmd[:-1] + ");"

                cursor.execute(sql_cmd, fields)
                self.connection.commit()
            else:
                raise TypeError("'record' must be dict")

            return True

        # raise OperationalError if the given table not exists
        raise sqlite3.OperationalError("no such table: {}".format(table))

    def get_record(self, table:str, primary_key, database:str=""):
        """Get row data / record from a table using the primary key."""
        if self.connection == "" and not database:
            raise TypeError("get_record() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            sql_cmd = "SELECT * FROM " + table + " WHERE " + self.get_primary_key(table=table, database=database) + "=?;"
            fetch = cursor.execute(sql_cmd, (primary_key,))

            # get columns list using get_columns
            columns = self.get_columns(table=table, database=database)
            record = {}

            try:
                for index, data in enumerate(fetch.fetchall()[0]):
                    # this creates dictionary with column names and records
                    record[columns[index]] = data
            except IndexError:
                # if the table does not have the requested data it returns
                # a empty list. so above for loop will raise an IndexError.
                return {}

            return record

        # raise OperationalError if the given table not exists
        raise sqlite3.OperationalError("no such table: {}".format(table))

    def get_all_records(self, table:str, database:str=""):
        """Get all data / records of a table."""
        if self.connection == "" and not database:
            raise TypeError("get_all_records() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            sql_cmd = "SELECT * FROM " + table
            cursor.execute(sql_cmd)
            rows = cursor.fetchall()

            # get columns list using get_columns
            columns = self.get_columns(table=table, database=database)
            records = []
            tmp_dict = {}

            for row in rows:
                for index, data in enumerate(row):
                    # this creates dictionary with column names and records
                    tmp_dict[columns[index]] = data
                records.append(tmp_dict)
                tmp_dict = {}

            return records

        # raise OperationalError if the given table not exists
        raise sqlite3.OperationalError("no such table: {}".format(table))

    def delete_record(self, table:str, primary_key, database:str=""):
        """Delete record from a table."""
        if self.connection == "" and not database:
            raise TypeError("delete_record() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()
            sql = "DELETE FROM " + table + " WHERE " + self.get_primary_key(table=table, database=database) + "=?"
            cursor.execute(sql, (primary_key,))
            self.connection.commit()

            return True

        # raise OperationalError if the given table not exists
        raise sqlite3.OperationalError("no such table: {}".format(table))

    def filter_records(self, table:str, values:dict, database:str=""):
        """
        Get filtered record list from a table.

        This will return one or more records by checking the values.
        """
        if self.connection == "" and not database:
            raise TypeError("filter_records() missing 1 required positional argument: 'database'")

        if database:
            self.create_connection(database)

        if self.is_table(table_name=table, database=database):
            cursor = self.connection.cursor()

            operators = [">", "<", "!", "="]

            sql = "SELECT * FROM " + table + " WHERE "

            for value in values:
                try:
                    # if value is in string type
                    # checks for if value contains any special character
                    if any(c in operators for c in values[value]):
                        sql += value + values[value] + " AND "
                    else:
                        sql += value + "='" + values[value] + "' AND "

                except TypeError:
                    # if value is in int or float type
                    sql += value + "=" + str(values[value]) + " AND "

            # removes unnecessary characters and completes the SQL command
            sql = sql[:-5] + ";"

            cursor.execute(sql)
            rows = cursor.fetchall()

            columns = self.get_columns(table=table, database=database)
            records = []
            tmp_dict = {}

            for row in rows:
                for index, data in enumerate(row):
                    # this creates dictionary with column names and records
                    tmp_dict[columns[index]] = data
                records.append(tmp_dict)
                tmp_dict = {}

            return records

        # raise OperationalError if the given table not exists
        raise sqlite3.OperationalError("no such table: {}".format(table))

    def close_connection(self):
        """Close the connection with the SQLite database file."""
        self.connection.close()
        return True
