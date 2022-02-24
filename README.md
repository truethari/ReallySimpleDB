<h1>
ReallySimpleDB 🧩
</h1>

<img src="https://raw.githubusercontent.com/truethari/ReallySimpleDB/master/assets/images/ReallySimpleDB.png" alt="Icon" width="465"> </img>

[![tests](https://github.com/truethari/ReallySimpleDB/actions/workflows/tests.yml/badge.svg?branch=alpha)](https://github.com/truethari/ReallySimpleDB/actions/workflows/tests.yml) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/befe3049923e4e788f5a1d6d958f6015)](https://www.codacy.com/gh/truethari/ReallySimpleDB/dashboard?utm_source=github.com&utm_medium=referral&utm_content=truethari/ReallySimpleDB&utm_campaign=Badge_Grade) [![PyPI version](https://img.shields.io/pypi/v/ReallySimpleDB.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/ReallySimpleDB/) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Downloads](https://pepy.tech/badge/reallysimpledb)](https://pepy.tech/project/reallysimpledb)

## What is This

---

This is a Python application that can be used to manage **sqlite** databases without using any sql command.

## 🚀 Installation

You can use pip:

```console
~$ pip3 install ReallySimpleDB
```

or

```console
~$ python setup.py install
```

## 📗 Usage

```console
>> from ReallySimpleDB import dbmanager

>> _dbmanager = dbmanager()
```

### Create database

```console
>> _dbmanager.create_db(dbpath="test.db", replace=True)
```

### Close connection

```console
>> _dbmanager.close_connection()
```

### Create table

Here you can not directly call the `create_table` function. Because **sqlite** cannot create table without columns. So you must first define the columns and create a table.

**Important:** You have to close connection here. If not, code returns error. Because it tries to add column to existing table.

```console
>> _dbmanager.close_connection()
```

```console
>> _dbmanager.add_columns(column_name="student_id", primary_key=True)
>> _dbmanager.add_columns(column_name="name", not_null=True)
>> _dbmanager.add_columns(column_name="mark", datatype="INT")

>> _dbmanager.create_table(database="test.db", table_name="STUDENTS")
```

If you want to add columns to an existing table, read the **Add column to table** section.

### Get all tables

```console
>> all_tables = _dbmanager.all_tables()

["STUDENT", "EXAM"]
```

### Check table if exists

```console
>> _dbmanager.is_table(database="test.db", table_name="STUDENTS")

True
```

### Delete table from database

```console
>> _dbmanager.delete_table(table="STUDENTS")
```

### Add column to table

```console
>> _dbmanager.add_columns(column_name="year", database="test.db", table="STUDENTS")
```

### Get all columns

```console
>> _dbmanager.get_columns(table="STUDENTS")

["student_id", "name", "mark"]
```

### Get all columns with types

```console
>> all_columns = _dbmanager.get_all_column_types(table="STUDENTS")

{"student_id": "TEXT", "name": "TEXT", "mark": "INT"}
```

### Get columns type

```console
>> _dbmanager.get_column_type(table="STUDENTS", column="student_id")

"TEXT"
```

### Get primary key of a table

```console
>> _dbmanager.get_primary_key(table="STUDENTS")

"student_id"
```

### Add record to table

```console
>> _dbmanager.add_record(table="STUDENTS", record={"student_id": "1010", "name":"ABC", "mark":10, "year":"2022"})
```

### Get all records from a table

```console
>> _dbmanager.get_all_records(table="STUDENTS", primary_key="1010")

[{'student_id': '1010', 'name': 'ABC', 'mark': 10, 'year': '2022'}, {'student_id': '1011', 'name': 'DEF', 'mark': 100, 'year': '2022'}]
```

### Get record from a table

```console
>> _dbmanager.get_record(table="STUDENTS", primary_key="1010")

{'student_id': '1010', 'name': 'ABC', 'mark': 10, 'year': '2022'}
```

### Delete record from a table

```console
>> _dbmanager.delete_record(table="STUDENTS", primary_key="1010")
```

### Filter record/s from a table

If you want to filter **equal values**, add value without any operator.

Examples:

- `{"year":2022}` ✔️
- `{"year":" == 2022"}` ❌

🖇 Comparison operators

| Comparison Operator |      Description      |
| :-----------------: | :-------------------: |
|         !=          |       Not Equal       |
|          >          |     Greater Than      |
|         >=          | Greater Than or Equal |
|          <          |       Less Than       |
|         <=          |  Less Than or Equal   |

Examples:

- `{"marks":"<= 10"}` ✔️
- `{"marks":"== 10"}` ❌
- `{"name":"< ABC"}` ❌ 'Greater Than' and 'Less than' comparisons are not supported with Strings

**Important:** If you are trying to compare strings, please use string between Inch Marks.

- `{"grade":"!= 'A'"}` ✔️
- `{"grade":"!= A"}` ❌

```console
>> _dbmanager.filter_records(table="STUDENTS", values={"year":"2022"})

[{'student_id': '1010', 'name': 'ABC', 'mark': 10, 'year': '2022'}, {'student_id': '1011', 'name': 'DEF', 'mark': 100, 'year': '2022'}]
```

---

## 🌱 Contributing Guide

- Fork the project from the `alpha` branch and submit a Pull Request (PR)

  - Explain what the PR fixes or improves.

  - If your PR aims to add a new feature, provide test functions as well.

- Use sensible commit messages

  - If your PR fixes a separate issue number, include it in the commit message.

- Use a sensible number of commit messages as well

  - e.g. Your PR should not have 1000s of commits.

### Run pytest without installing package

If you are adding **new functions** as described above, please add test functions to `tests/test_manager.py`.

```console
~$ python -m pytest -s tests
```
