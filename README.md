# ReallySimpleDB 🧩 [alpha]

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/09b9e60691484c29b4cac87178b8aaae)](https://www.codacy.com/gh/truethari/ReallySimpleDB/dashboard?utm_source=github.com&utm_medium=referral&utm_content=truethari/ReallySimpleDB&utm_campaign=Badge_Grade)

---

**🔧 This is still in development and may cause errors when using certain functions.**

---

## What is This

---

This is a Python application that can be used to manage **sqlite** databases without using any sql command.

## 🚀 Installation

You can use pip:

~~pip3 install ReallySimpleDB~~

or

```console
~# python setup.py install
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

Important: You have to close connection here. If not, code returns error. Because it tries to add column to existing table.

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

### Add record to table

```console
>> _dbmanager.add_record(table="STUDENTS", record={"student_id": "1010", "name":"ABC", "mark":10, "year":"2022"})
```

## 🌱 Contributing Guide

- Fork the project from the `alpha` branch and submit a Pull Request (PR)

  - Explain what the PR fixes or improves.

  - If your PR aims to add a new feature, provide test functions as well.

- Use sensible commit messages

  - If your PR fixes a separate issue number, include it in the commit message.

- Use a sensible number of commit messages as well

  - e.g. Your PR should not have 1000s of commits.
