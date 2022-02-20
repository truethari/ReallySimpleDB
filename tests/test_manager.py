from ast import Assert
import os
from ReallySimpleDB import dbmanager

_dbmanager = dbmanager()

def test_create_db():
    assert _dbmanager.create_db(dbpath="test.db", replace=True)
    delete_db()

def test_create_table_1():
    _dbmanager.create_db(dbpath="test.db", replace=True)
    _dbmanager.close_connection()

    _dbmanager.add_columns(column_name="student_id", primary_key=True)
    _dbmanager.add_columns(column_name="name", not_null=True)
    _dbmanager.add_columns(column_name="mark", datatype="INT")
    assert _dbmanager.create_table(database="test.db", table_name="STUDENTS")

def test_create_table_2():
    _dbmanager.clean()
    _dbmanager.add_columns(column_name="teacher_id", primary_key=True)
    _dbmanager.add_columns(column_name="name", not_null=True)
    _dbmanager.add_columns(column_name="number", datatype="INT")
    assert _dbmanager.create_table(database="test.db", table_name="TEACHERS")

def test_create_table_3():
    _dbmanager.clean()
    _dbmanager.add_columns(column_name="emp_id", primary_key=True)
    _dbmanager.add_columns(column_name="name", not_null=True)
    _dbmanager.add_columns(column_name="number", datatype="INT")
    assert _dbmanager.create_table(table_name="EMPLOYEES")

def test_add_columns():
    assert _dbmanager.add_columns(column_name="year", database="test.db", table="STUDENTS")

def test_all_tables_1():
    assert "STUDENTS" in _dbmanager.all_tables("test.db")

def test_all_tables_2():
    assert "NON" not in _dbmanager.all_tables("test.db")

def test_all_tables_3():
    assert "STUDENTS" in _dbmanager.all_tables()

def test_all_tables_4():
    assert "NON" not in _dbmanager.all_tables()

def test_is_table_1():
    assert _dbmanager.is_table(database="test.db", table_name="STUDENTS")

def test_is_table_2():
    assert not _dbmanager.is_table(database="test.db", table_name="NON")

def test_is_table_3():
    assert _dbmanager.is_table(table_name="STUDENTS")

def test_is_table_4():
    assert not _dbmanager.is_table(table_name="NON")

def test_delete_table_1():
    assert _dbmanager.delete_table(table="EMPLOYEES")

def test_delete_table_2():
    assert not _dbmanager.delete_table(table="EMPLOYEES")

def test_get_all_column_types_1():
    assert _dbmanager.get_all_column_types(table="STUDENTS") \
        == {"student_id": "TEXT", "name": "TEXT", "mark": "INT", "year": "TEXT"}

def test_get_all_column_types_2():
    assert _dbmanager.get_all_column_types(table="STUDENTS") \
        != {"student_id": "FF", "name": "FF", "FF": "FF", "FF": "FF"}

def test_get_column_type_1():
    assert _dbmanager.get_column_type(table="STUDENTS", column="student_id") == "TEXT"

def test_get_column_type_2():
    assert _dbmanager.get_column_type(table="STUDENTS", column="address") == False

def test_get_column_type_3():
    assert _dbmanager.get_column_type(table="EMPLOYEES", column="emp_id") == False

def test_get_columns_1():
    assert _dbmanager.get_columns(table="STUDENTS") == ["student_id", "name", "mark", "year"]

def test_get_columns_2():
    assert _dbmanager.get_columns(table="EMPLOYEES") == []

def test_get_primary_key_1():
    assert _dbmanager.get_primary_key(table="STUDENTS") == "student_id"

def test_get_primary_key_2():
    assert _dbmanager.get_primary_key(table="TEACHERS") == "teacher_id"

def test_add_record_1():
    assert _dbmanager.add_record(table="STUDENTS", record={"student_id": "1010", "name":"ABC", "mark":10, "year":"2022"}) == True

def test_add_record_2():
    try:
        _dbmanager.add_record(table="STUDENTS", record={"student_id": 10, "name":"ABC", "mark":10, "year":"2022"})
        assert False
    except TypeError:
        assert True

def test_finally():
    delete_db()

def delete_db(database="test.db"):
    _dbmanager.close_connection()
    os.remove(database)
