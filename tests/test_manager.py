import os
from sqlite3 import OperationalError
from ReallySimpleDB import dbmanager

_dbmanager = dbmanager()

def test_create_db():
    """Create new database."""
    assert _dbmanager.create_db(dbpath="test.db", replace=True)
    delete_db()

def test_create_table_1():
    """Create new database and new table with columns."""
    _dbmanager.create_db(dbpath="test.db", replace=True)
    _dbmanager.close_connection()

    _dbmanager.add_columns(column_name="student_id", primary_key=True)
    _dbmanager.add_columns(column_name="name", not_null=True)
    _dbmanager.add_columns(column_name="mark", datatype="INT")
    assert _dbmanager.create_table(database="test.db", table_name="STUDENTS")

def test_create_table_2():
    """Create new table with columns."""
    _dbmanager.clean()
    _dbmanager.add_columns(column_name="teacher_id", primary_key=True)
    _dbmanager.add_columns(column_name="name", not_null=True)
    _dbmanager.add_columns(column_name="number", datatype="INT")
    assert _dbmanager.create_table(database="test.db", table_name="TEACHERS")

def test_create_table_3():
    """Create new table with columns."""
    _dbmanager.clean()
    _dbmanager.add_columns(column_name="emp_id", primary_key=True)
    _dbmanager.add_columns(column_name="name", not_null=True)
    _dbmanager.add_columns(column_name="number", datatype="INT")
    assert _dbmanager.create_table(table_name="EMPLOYEES")

def test_add_columns():
    """Add new column to a table."""
    assert _dbmanager.add_columns(column_name="year", database="test.db", table="STUDENTS")

def test_all_tables_1():
    """If table exists in the database."""
    assert "STUDENTS" in _dbmanager.all_tables("test.db")

def test_all_tables_2():
    """If table not in the database."""
    assert "NON" not in _dbmanager.all_tables("test.db")

def test_all_tables_3():
    """If table exists in the database.. without define the db."""
    assert "STUDENTS" in _dbmanager.all_tables()

def test_all_tables_4():
    """If table not in the database.. without define the db."""
    assert "NON" not in _dbmanager.all_tables()

def test_is_table_1():
    """Check if the given table is exists in the database."""
    assert _dbmanager.is_table(database="test.db", table_name="STUDENTS")

def test_is_table_2():
    """Check if the given table is not in the database."""
    assert not _dbmanager.is_table(database="test.db", table_name="NON")

def test_is_table_3():
    """Check if the given table is exists in the database.. without define the db."""
    assert _dbmanager.is_table(table_name="STUDENTS")

def test_is_table_4():
    """Check if the given table is not in the database.. without define the db."""
    assert not _dbmanager.is_table(table_name="NON")

def test_delete_table_1():
    """Delete table if table exists."""
    try:
        _dbmanager.delete_table(table="EMPLOYEES")
        assert True
    except OperationalError:
        assert False

def test_delete_table_2():
    """Delete table if table not exists."""
    try:
        _dbmanager.delete_table(table="EMPLOYEES")
        assert False
    except OperationalError:
        assert True

def test_get_all_column_types_1():
    """Get all the column names with the data types in a table."""
    assert _dbmanager.get_all_column_types(table="STUDENTS") \
        == {"student_id": "TEXT", "name": "TEXT", "mark": "INT", "year": "TEXT"}

def test_get_column_type_1():
    """Get data type of a column in a table."""
    assert _dbmanager.get_column_type(table="STUDENTS", column="student_id") == "TEXT"

def test_get_column_type_2():
    """Get data type of not exists column in a table."""
    try:
        _dbmanager.get_column_type(table="STUDENTS", column="address")
        assert False
    except OperationalError:
        assert True

def test_get_columns_1():
    """Get all the column names list in a table."""
    assert _dbmanager.get_columns(table="STUDENTS") == ["student_id", "name", "mark", "year"]

def test_get_primary_key_1():
    """Find and get primary key of a table."""
    assert _dbmanager.get_primary_key(table="STUDENTS") == "student_id"

def test_get_primary_key_2():
    """Find and get primary key of a table."""
    assert _dbmanager.get_primary_key(table="TEACHERS") == "teacher_id"

def test_add_record_1():
    """Add a new record to a table."""
    assert _dbmanager.add_record(table="STUDENTS", record={"student_id": "1010", "name":"ABC", "mark":10, "year":"2022"}) == True

def test_add_record_2():
    """Add a new record to a table."""
    assert _dbmanager.add_record(table="STUDENTS", record={"student_id": "1011", "name":"DEF", "mark":100, "year":"2022"}) == True

def test_add_record_3():
    """Add a new record to a table with datatype errors."""
    try:
        _dbmanager.add_record(table="STUDENTS", record={"student_id": 10, "name":"ABC", "mark":10, "year":"2022"})
        assert False
    except TypeError:
        assert True

def test_get_record_1():
    """Get row data / record from a table using the primary key."""
    assert _dbmanager.get_record(table="STUDENTS", primary_key="1010") == {'student_id': '1010', 'name': 'ABC', 'mark': 10, 'year': '2022'}

def test_get_record_2():
    """Get row data / record from a table using the primary key."""
    assert _dbmanager.get_record(table="STUDENTS", primary_key="10101") == {}

def test_get_all_records():
    """Get all data / records of a table."""
    assert _dbmanager.get_all_records(table="STUDENTS") == [{'student_id': '1010', 'name': 'ABC', 'mark': 10, 'year': '2022'},
        {'student_id': '1011', 'name': 'DEF', 'mark': 100, 'year': '2022'}]

def test_filter_record_1():
    """Get filtered record list from a table."""
    assert _dbmanager.filter_records(table="STUDENTS", values={"year":"2022"}) == [{'student_id': '1010', 'name': 'ABC', 'mark': 10, 'year': '2022'},
        {'student_id': '1011', 'name': 'DEF', 'mark': 100, 'year': '2022'}]

def test_filter_record_2():
    """Get filtered record list from a table."""
    assert _dbmanager.filter_records(table="STUDENTS", values={"mark":100, "year":"2022"}) == [{'student_id': '1011', 'name': 'DEF', 'mark': 100, 'year': '2022'}]

def test_filter_record_3():
    """Get filtered record list from a table: Comparison."""
    assert _dbmanager.filter_records(table="STUDENTS", values={"mark":" <= 100"}) == [{'student_id': '1010', 'name': 'ABC', 'mark': 10, 'year': '2022'}, {'student_id': '1011', 'name': 'DEF', 'mark': 100, 'year': '2022'}]

def test_filter_record_4():
    """Get filtered record list from a table: Comparison."""
    assert _dbmanager.filter_records(table="STUDENTS", values={"mark":" != 100"}) == [{'student_id': '1010', 'name': 'ABC', 'mark': 10, 'year': '2022'}]

def test_delete_record_1():
    """Delete record from a table."""
    assert _dbmanager.delete_record(table="STUDENTS", primary_key="1010")

def test_delete_record_2():
    """Delete record from a table when table is not exists."""
    try:
        _dbmanager.delete_record(table="STUDENTSS", primary_key="1010")
        assert False
    except OperationalError:
        assert True

def test_finally():
    """Delete the database."""
    delete_db()

def delete_db(database="test.db"):
    """Close connection and deletes the database."""
    _dbmanager.close_connection()
    os.remove(database)
