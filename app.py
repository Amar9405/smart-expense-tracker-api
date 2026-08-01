from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=date.today)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    selected_category = request.args.get("category", "").strip()
    start_date_str = request.args.get("start_date", "").strip()
    end_date_str = request.args.get("end_date", "").strip()

    query = db.select(Expense).order_by(Expense.date.desc())
    if selected_category:
        query = query.where(Expense.category == selected_category)

    start_date = None
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            query = query.where(Expense.date >= start_date)
        except ValueError:
            pass

    end_date = None
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            query = query.where(Expense.date <= end_date)
        except ValueError:
            pass

    expenses = db.session.scalars(query).all()

    total_expense = sum(expense.amount for expense in expenses)
    today = date.today()
    today_expense = sum(
        expense.amount for expense in expenses if expense.date == today
    )
    month_expense = sum(
        expense.amount for expense in expenses if expense.date and expense.date.year == today.year and expense.date.month == today.month
    )

    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

    daily_totals = {}
    for expense in expenses:
        expense_date = expense.date.strftime('%Y-%m-%d') if expense.date else today.strftime('%Y-%m-%d')
        daily_totals[expense_date] = daily_totals.get(expense_date, 0) + expense.amount

    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "index.html",
        expenses=expenses,
        messages=messages,
        total_expense=total_expense,
        today_expense=today_expense,
        month_expense=month_expense,
        category_totals=category_totals,
        daily_totals=daily_totals,
        selected_category=selected_category,
        selected_start_date=start_date_str,
        selected_end_date=end_date_str,
    )


@app.route("/add", methods=["POST"])
def add():

    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not description or not amount_str or not category:
        flash("Please fill description, amount and category", "error")
        return redirect(url_for("index"))

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be a positive number", "error")
        return redirect(url_for("index"))

    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        d = date.today()

    e = Expense(
        description=description,
        amount=amount,
        category=category,
        date=d
    )

    db.session.add(e)
    db.session.commit()

    flash("Expense added", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    expense = db.session.get(Expense, expense_id)
    if expense is not None:
        db.session.delete(expense)
        db.session.commit()
        flash("Expense deleted", "success")
    else:
        flash("Expense not found", "error")
    return redirect(url_for("index"))


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit(expense_id):
    expense = db.session.get(Expense, expense_id)
    if expense is None:
        flash("Expense not found", "error")
        return redirect(url_for("index"))

    categories = ["Food", "Transport", "Rent", "Utilities", "Shopping", "Entertainment"]

    if request.method == "POST":
        description = (request.form.get("description") or "").strip()
        amount_str = (request.form.get("amount") or "").strip()
        category = (request.form.get("category") or "").strip()
        date_str = (request.form.get("date") or "").strip()

        if not description or not amount_str or not category:
            flash("Please fill description, amount and category", "error")
            return redirect(url_for("edit", expense_id=expense.id))

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Amount must be a positive number", "error")
            return redirect(url_for("edit", expense_id=expense.id))

        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
        except ValueError:
            d = date.today()

        expense.description = description
        expense.amount = amount
        expense.category = category
        expense.date = d
        db.session.commit()
        flash("Expense updated", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", expense=expense, categories=categories, today=date.today())


if __name__ == "__main__":
    app.run(debug=True, port=4848)