import pytest
import os
from ReallySimpleDB import dbmanager

_dbmanager = dbmanager()

def test_create_db():
    value = _dbmanager.create_db("test.db")
    if value:
        _dbmanager.close_connection()
        os.remove("test.db")
    assert value
