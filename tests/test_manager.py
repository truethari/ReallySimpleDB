import os
from ReallySimpleDB import dbmanager

_dbmanager = dbmanager()

def test_create_db():
    if _dbmanager.create_db("test.db", replace=True):
        _dbmanager.close_connection()
        os.remove("test.db")
        assert True

def test_create_table():
    _dbmanager.create_db("test.db", replace=True)
    _dbmanager.close_connection()

    _dbmanager.add_columns(column_name="student_id", primary_key=True)
    _dbmanager.add_columns(column_name="name", NOT_NULL=True)
    _dbmanager.add_columns(column_name="mark", datatype="INT")
    if _dbmanager.create_table(database="test.db", table_name="STUDENTS"):
        _dbmanager.close_connection()
        assert True

def test_add_columns():
    if _dbmanager.add_columns(column_name="year", database="test.db", table="STUDENTS"):
        _dbmanager.close_connection()
        os.remove("test.db")
        assert True
