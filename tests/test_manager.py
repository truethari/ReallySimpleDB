import os
from ReallySimpleDB import dbmanager

_dbmanager = dbmanager()

def test_create_db():
    assert _dbmanager.create_db("test.db", replace=True)
    delete_db()

def test_create_table():
    _dbmanager.create_db("test.db", replace=True)
    _dbmanager.close_connection()

    _dbmanager.add_columns(column_name="student_id", primary_key=True)
    _dbmanager.add_columns(column_name="name", NOT_NULL=True)
    _dbmanager.add_columns(column_name="mark", datatype="INT")
    assert _dbmanager.create_table(database="test.db", table_name="STUDENTS")

def test_add_columns():
    assert _dbmanager.add_columns(column_name="year", database="test.db", table="STUDENTS")

def test_all_tables_1():
    assert "STUDENTS" in _dbmanager.all_tables("test.db")

def test_all_tables_2():
    assert "NON" not in _dbmanager.all_tables("test.db")

def test_is_table_1():
    assert _dbmanager.is_table("test.db", "STUDENTS")

def test_is_table_2():
    assert not _dbmanager.is_table("test.db", "NON")
    delete_db()

def delete_db(database="test.db"):
    _dbmanager.close_connection()
    os.remove(database)
