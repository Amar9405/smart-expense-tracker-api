from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    get_flashed_messages,
    session
)

from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from dotenv import load_dotenv

from datetime import date, datetime, timedelta
import secrets
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Email configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

db = SQLAlchemy(app)

mail = Mail(app)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:
            flash("Please login to continue.", "error")
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view

def guest_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "user_id" in session:
            return redirect(url_for("index"))

        return view(*args, **kwargs)

    return wrapped_view

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    expenses = db.relationship(
        "Expense",
        backref="user",
        lazy=True
    )
    
class PasswordResetOTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    otp_hash = db.Column(
        db.String(255),
        nullable=False
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    attempts = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    used = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "password_reset_otps",
            lazy=True
        )
    )
    
def generate_reset_otp(user_id):
    # Generate a secure 6-digit OTP
    otp = f"{secrets.randbelow(1000000):06d}"

    # Remove previous unused OTPs for this user
    old_otps = db.session.scalars(
        db.select(PasswordResetOTP).where(
            PasswordResetOTP.user_id == user_id,
            PasswordResetOTP.used == False
        )
    ).all()

    for old_otp in old_otps:
        old_otp.used = True

    # Create OTP that expires after 10 minutes
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    reset_otp = PasswordResetOTP(
        user_id=user_id,
        otp_hash=generate_password_hash(otp),
        expires_at=expires_at,
        attempts=0,
        used=False
    )

    db.session.add(reset_otp)
    db.session.commit()

    return otp


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=date.today)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


with app.app_context():
    db.create_all()


@app.route("/")
@login_required
def index():
    
    selected_category = request.args.get("category", "").strip()
    start_date_str = request.args.get("start_date", "").strip()
    end_date_str = request.args.get("end_date", "").strip()

    query = (
        db.select(Expense)
        .where(Expense.user_id == session["user_id"])
        .order_by(Expense.date.desc())
    )
    
    
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
@login_required
def add():
    # Make sure user is logged in
    if "user_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("login"))

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
        d = (
            datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_str
            else date.today()
        )

    except ValueError:
        d = date.today()

    # Create expense for logged-in user
    expense = Expense(
        description=description,
        amount=amount,
        category=category,
        date=d,
        user_id=session["user_id"]
    )

    db.session.add(expense)
    db.session.commit()

    flash("Expense added successfully", "success")

    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete(expense_id):

    # User must be logged in
    if "user_id" not in session:
        flash("Please login to continue.", "error")
        return redirect(url_for("login"))

    # Find expense belonging to the logged-in user
    expense = db.session.scalar(
        db.select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == session["user_id"]
        )
    )

    if expense is None:
        flash("Expense not found or you do not have permission to delete it.", "error")
        return redirect(url_for("index"))

    db.session.delete(expense)
    db.session.commit()

    flash("Expense deleted successfully.", "success")

    return redirect(url_for("index"))

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit(expense_id):

    # User must be logged in
    if "user_id" not in session:
        flash("Please login to continue.", "error")
        return redirect(url_for("login"))

    # Find only the expense belonging to the logged-in user
    expense = db.session.scalar(
        db.select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == session["user_id"]
        )
    )

    if expense is None:
        flash(
            "Expense not found or you do not have permission to edit it.",
            "error"
        )
        return redirect(url_for("index"))

    categories = [
        "Food",
        "Transport",
        "Rent",
        "Utilities",
        "Shopping",
        "Entertainment"
    ]

    if request.method == "POST":

        description = (
            request.form.get("description") or ""
        ).strip()

        amount_str = (
            request.form.get("amount") or ""
        ).strip()

        category = (
            request.form.get("category") or ""
        ).strip()

        date_str = (
            request.form.get("date") or ""
        ).strip()

        if not description or not amount_str or not category:
            flash(
                "Please fill description, amount and category",
                "error"
            )
            return redirect(
                url_for("edit", expense_id=expense.id)
            )

        try:
            amount = float(amount_str)

            if amount <= 0:
                raise ValueError

        except ValueError:
            flash(
                "Amount must be a positive number",
                "error"
            )
            return redirect(
                url_for("edit", expense_id=expense.id)
            )

        try:
            d = (
                datetime.strptime(
                    date_str,
                    "%Y-%m-%d"
                ).date()
                if date_str
                else date.today()
            )

        except ValueError:
            d = date.today()

        # Update expense
        expense.description = description
        expense.amount = amount
        expense.category = category
        expense.date = d

        db.session.commit()

        flash(
            "Expense updated successfully.",
            "success"
        )

        return redirect(url_for("index"))

    return render_template(
        "edit.html",
        expense=expense,
        categories=categories,
        today=date.today()
    )

@app.route("/register", methods=["GET", "POST"])
@guest_only
def register():

    if request.method == "GET":
        return render_template("register.html")

    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    confirm_password = request.form.get("confirm_password") or ""

    # Basic validation
    if not name or not email or not password or not confirm_password:
        flash("Please fill all fields.", "error")
        return redirect(url_for("register"))

    # Password length
    if len(password) < 8:
        flash("Password must be at least 8 characters.", "error")
        return redirect(url_for("register"))

    # Password confirmation
    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect(url_for("register"))

    # Check existing email
    existing_user = db.session.scalar(
        db.select(User).where(User.email == email)
    )

    if existing_user:
        flash("An account with this email already exists.", "error")
        return redirect(url_for("register"))

    # Hash password
    password_hash = generate_password_hash(password)

    # Create user
    user = User(
        name=name,
        email=email,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    flash("Registration successful! You can now login.", "success")

    return redirect(url_for("register"))

@app.route("/forgot-password", methods=["GET", "POST"])
@guest_only
def forgot_password():

    if request.method == "GET":
        return render_template("forgot_password.html")

    email = (request.form.get("email") or "").strip().lower()

    if not email:
        flash("Please enter your email address.", "error")
        return redirect(url_for("forgot_password"))

    user = db.session.scalar(
        db.select(User).where(User.email == email)
    )

    if user is None:
        flash(
            "If an account exists with this email, "
            "a verification code will be sent.",
            "success"
        )
        return redirect(url_for("forgot_password"))

    # Generate OTP
    otp = generate_reset_otp(user.id)
    
    # Remember user for OTP verification
    session["reset_user_id"] = user.id
    session["otp_verified"] = False
    
    

    # Send OTP through email
    message = Message(
        subject="SpendIQ Password Reset Code",
        recipients=[user.email]
    )

    message.body = f"""
Hello {user.name},

We received a request to reset your SpendIQ password.

Your verification code is:

{otp}

This code will expire in 10 minutes.

If you did not request a password reset, you can safely ignore this email.

Regards,
SpendIQ Team
"""

    mail.send(message)

    flash(
        "If an account exists with this email, "
        "a verification code has been sent.",
        "success"
    )

    return redirect(url_for("verify_otp"))

@app.route("/verify-otp", methods=["GET", "POST"])
@guest_only
def verify_otp():

    # User must come here after requesting a password reset
    reset_user_id = session.get("reset_user_id")

    if not reset_user_id:
        flash(
            "Please request a password reset first.",
            "error"
        )
        return redirect(url_for("forgot_password"))

    # Show OTP page
    if request.method == "GET":
        return render_template("verify_otp.html")

    # Get OTP entered by user
    otp = (request.form.get("otp") or "").strip()

    # Basic OTP validation
    if not otp:
        flash(
            "Please enter the verification code.",
            "error"
        )
        return redirect(url_for("verify_otp"))

    if not otp.isdigit() or len(otp) != 6:
        flash(
            "Please enter a valid 6-digit verification code.",
            "error"
        )
        return redirect(url_for("verify_otp"))

    # Get latest unused OTP for this user
    reset_otp = db.session.scalar(
        db.select(PasswordResetOTP)
        .where(
            PasswordResetOTP.user_id == reset_user_id,
            PasswordResetOTP.used == False
        )
        .order_by(
            PasswordResetOTP.created_at.desc()
        )
    )

    # OTP not found
    if reset_otp is None:
        flash(
            "Verification code not found. Please request a new code.",
            "error"
        )
        return redirect(url_for("forgot_password"))

    # Maximum 5 attempts
    if reset_otp.attempts >= 5:

        reset_otp.used = True
        db.session.commit()

        flash(
            "Too many incorrect attempts. Please request a new code.",
            "error"
        )

        return redirect(url_for("forgot_password"))

    # Check OTP expiration
    if datetime.utcnow() > reset_otp.expires_at:

        reset_otp.used = True
        db.session.commit()

        flash(
            "This verification code has expired. Please request a new one.",
            "error"
        )

        return redirect(url_for("forgot_password"))

    # Verify OTP
    if not check_password_hash(
        reset_otp.otp_hash,
        otp
    ):

        reset_otp.attempts += 1
        db.session.commit()

        remaining_attempts = 5 - reset_otp.attempts

        if remaining_attempts <= 0:

            reset_otp.used = True
            db.session.commit()

            flash(
                "Too many incorrect attempts. Please request a new code.",
                "error"
            )

            return redirect(url_for("forgot_password"))

        flash(
            f"Incorrect verification code. "
            f"{remaining_attempts} attempts remaining.",
            "error"
        )

        return redirect(url_for("verify_otp"))

    # ==================================================
    # OTP IS CORRECT
    # ==================================================

    # Get the user
    user = db.session.get(
        User,
        reset_user_id
    )

    if user is None:

        session.clear()

        flash(
            "User account not found.",
            "error"
        )

        return redirect(url_for("login"))

    # Mark OTP as used
    reset_otp.used = True

    # Clear old reset session
    session.clear()

    # Create login session
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["user_email"] = user.email

    # Save OTP status
    db.session.commit()

    flash(
        "OTP verified successfully. Welcome back!",
        "success"
    )

    # Automatically login and go to dashboard
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
@guest_only
def login():

    if request.method == "GET":
        return render_template("login.html")

    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    if not email or not password:
        flash("Please enter your email and password.", "error")
        return redirect(url_for("login"))

    user = db.session.scalar(
        db.select(User).where(User.email == email)
    )

    if user is None:
        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    if not check_password_hash(user.password_hash, password):
        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    # Create login session
    session.clear()

    session["user_id"] = user.id
    session["user_name"] = user.name
    session["user_email"] = user.email

    flash(f"Welcome back, {user.name}!", "success")

    return redirect(url_for("index"))

@app.route("/account")
@login_required
def account():
    user = db.session.get(User, session["user_id"])

    if user is None:
        session.clear()
        flash("User account not found.", "error")
        return redirect(url_for("login"))

    return render_template(
        "account.html",
        user=user
    )
    
@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    user = db.session.get(User, session["user_id"])

    if user is None:
        session.clear()
        flash("User account not found.", "error")
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("change_password.html")

    current_password = request.form.get("current_password") or ""
    new_password = request.form.get("new_password") or ""
    confirm_password = request.form.get("confirm_password") or ""

    # Check all fields
    if not current_password or not new_password or not confirm_password:
        flash("Please fill all password fields.", "error")
        return redirect(url_for("change_password"))

    # Verify current password
    if not check_password_hash(user.password_hash, current_password):
        flash("Current password is incorrect.", "error")
        return redirect(url_for("change_password"))

    # Check new password length
    if len(new_password) < 8:
        flash("New password must be at least 8 characters.", "error")
        return redirect(url_for("change_password"))

    # Check password confirmation
    if new_password != confirm_password:
        flash("New passwords do not match.", "error")
        return redirect(url_for("change_password"))

    # Prevent same password
    if check_password_hash(user.password_hash, new_password):
        flash("New password must be different from your current password.", "error")
        return redirect(url_for("change_password"))

    # Generate new password hash
    user.password_hash = generate_password_hash(new_password)

    db.session.commit()

    flash("Your password has been changed successfully.", "success")

    return redirect(url_for("account"))

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("login"))




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4848))
    app.run(host="0.0.0.0", debug=True ,port=port)