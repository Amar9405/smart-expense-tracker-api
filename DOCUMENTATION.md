# Smart Expense Tracker API Documentation


## Project Overview

The Smart Expense Tracker API is a RESTful web application developed using Python and Flask. It is designed to help users manage their personal expenses by providing simple endpoints to add, retrieve, filter, calculate, and delete expense records.

The goal of this project is to demonstrate the fundamentals of REST API development, request validation, database integration, and clean project organization. The application stores expense data locally using SQLite through SQLAlchemy ORM.

---

# Objectives

The main objectives of this project are:

* Build a REST API using Flask.
* Perform CRUD operations on expense records.
* Validate user input before storing data.
* Organize the project using a clean folder structure.
* Provide a simple and maintainable codebase.

---

# Features

The application currently supports the following features:

* Add a new expense.
* View all expenses.
* Filter expenses by category.
* Calculate total expenses.
* Calculate total expenses by category.
* Delete an existing expense.
* Input validation with meaningful error messages.
* SQLite database integration using SQLAlchemy.

---

# Technology Stack

Backend

* Python
* Flask
* Flask-SQLAlchemy

Database

* SQLite

Frontend

* HTML
* Tailwind CSS

Other Tools

* Git
* GitHub

---

# Project Structure

```text
your-repo/
│
├── README.md
├── AI_NOTES.md
├── DOCUMENTATION.md
├── requirements.txt
│
├── src/
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   └── ...
│
└── tests/
    └── test_api.py
```

---

# Database Schema

The project uses a single table named **Expense**.

| Field       | Type    | Description                |
| ----------- | ------- | -------------------------- |
| id          | Integer | Unique identifier          |
| description | String  | Description of the expense |
| amount      | Float   | Expense amount             |
| category    | String  | Expense category           |
| date        | Date    | Date of the expense        |

---

# API Endpoints

## Add Expense

**POST**

```text
/expenses
```

Adds a new expense record.

---

## View All Expenses

**GET**

```text
/expenses
```

Returns all stored expenses.

---

## Filter Expenses

**GET**

```text
/expenses?category=Food
```

Returns expenses that belong to the selected category.

---

## Calculate Total Expenses

**GET**

```text
/expenses/total
```

Returns the sum of all expenses.

---

## Calculate Total by Category

**GET**

```text
/expenses/total?category=Food
```

Returns the total amount spent in a particular category.

---

## Delete Expense

**DELETE**

```text
/expenses/<id>
```

Deletes an expense using its unique ID.

---

# Validation

The application performs basic validation before storing data.

Validation rules include:

* Description cannot be empty.
* Amount must be greater than zero.
* Category cannot be empty.
* Date must be valid.

If validation fails, the application returns an appropriate error message.

---

# Error Handling

The application handles common errors such as:

* Missing required fields
* Invalid amount values
* Invalid date format
* Expense not found
* Invalid request parameters

These checks help prevent incorrect data from being stored.

---

# Testing

The application was tested locally to verify that:

* Expenses are added successfully.
* Expense data is stored correctly.
* All expenses can be retrieved.
* Category filtering works correctly.
* Total calculations return expected values.
* Expenses can be deleted without affecting other records.

---

# Future Improvements

Possible enhancements include:

* User authentication
* Monthly budget tracking
* Expense editing
* CSV or Excel export
* Dashboard analytics
* Monthly summary reports
* Docker support
* Cloud database integration

---

# Conclusion

This project demonstrates the implementation of a simple and maintainable REST API using Flask and SQLite. It follows a clean project structure, includes input validation and error handling, and provides the core functionality required for managing personal expenses.

The project was developed with a focus on readability, simplicity, and ease of maintenance while meeting the assignment requirements.
