#lottery web app!

Description

This project is a simple web application written in Python using the Flask and sqlite3 libraries. This program allows you to:

Store the  people data  in  sqlite3 database.

Enter a number of winner  as input.

Determine the winners of the lottery based on the number of people and the input number.

Program Pages

Home: This page allows you to enter the number of people and run the raffle.

upload to  Database Page: This page allows you to upload data to  database.

View Database Page: This page displays all the information in the database.

Delete from Database Page: This page allows you to delete table from the database.


Installation

Prerequisites:

Python 3.9 (https://www.python.org/downloads/)

pip (https://pip.pypa.io/en/stable/installation/)

Clone the project from GitHub:

```bash
git clone https://github.com/So-Ebrahimi/lottery_app.git
```

Go to the project folder:

```bash
cd lottery_app
```

Crate and Activate the Python virtual environment:
```bash
python -m venv .venv
```

```bash
cd .venv/Scripts
```
```bash
activat.bat 
```
Install the required libraries:
```bash
pip install -r requirements.txt
```

Run the program:
```bash
python app.py
```
Go to http://localhost:12345 in your browser.


Page Guide

Homepage:

In the "select table name" field, slect your table before you apload in database(table 1 is in db) .

In the "Enter number of winners" field, Enter the number of people who must win .

In the "Enter winner number" field, enter a number  in  range slice of total .

Click the submit Query.

The list of lttery winners will be displayed.

can download list with Download csv button 

view Database Page:

A list of all the information in the database is displayed.

upload Database Page:

upload xlsx file with "RAW" "NAME" "PHONE" collums and write your table name 

Delete  Database Page:

delete tables data 

Notes

This program is a simple example and you can extend it based on your needs.

For more information on the Flask and sqlite3 libraries, refer to their documentation.

Resources

Flask Documentation: https://flask.palletsprojects.com/en/2.2.x/

sqlite3 Documentation: https://docs.python.org/3/library/sqlite3.html