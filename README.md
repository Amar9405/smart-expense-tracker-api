# Smart Expense Tracker API

**Live Demo:** `<DEPLOYMENT_LINK>`

A REST API built with **Python**, **Flask**, and **Flask-SQLAlchemy** for managing personal expenses. The API allows users to add, view, filter, calculate totals, and delete expenses.

---

## Features

* Add a new expense
* View all expenses
* Filter expenses by category
* Calculate total expenses
* Calculate total expenses by category
* Delete an expense
* Input validation
* Error handling

---

## Tech Stack

* Python 3
* Flask
* Flask-SQLAlchemy
* SQLite

---

## Project Structure

```text
your-repo/
│── README.md
│── AI_NOTES.md
│── requirements.txt
│
├── src/
│   ├── app.py
│   └── ...
│
└── tests/
    └── test_api.py
```

---

## Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_LINK>
```

Go to the project directory:

```bash
cd your-repo
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Server

```bash
python src/app.py
```

The API will start on:

```text
http://127.0.0.1:5000
```

> If your application uses a different port (for example, `4848`), update the command accordingly.

---

## Run Tests

```bash
pytest
```

---

## API Endpoints

### Add Expense

**POST** `/expenses`

Example Request Body:

```json
{
  "title": "Groceries",
  "amount": 500,
  "category": "Food",
  "date": "2026-08-02"
}
```

---

### View All Expenses

**GET** `/expenses`

---

### Filter Expenses by Category

**GET** `/expenses?category=Food`

---

### Calculate Total Expenses

**GET** `/expenses/total`

---

### Calculate Total Expenses by Category

**GET** `/expenses/total?category=Food`

---

### Delete an Expense

**DELETE** `/expenses/<id>`

Example:

```text
DELETE /expenses/1
```

---

## Notes

* Expenses are stored locally using SQLite.
* The API returns JSON responses.
* Invalid requests are handled with appropriate error messages.

---

## Author

**Amar Sonawane**
