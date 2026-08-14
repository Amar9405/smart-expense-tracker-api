# SpendIQ - Smart Expense Tracker

A full-stack web application built with **Python**, **Flask**, and **Flask-SQLAlchemy** for managing personal expenses. SpendIQ allows users to securely register, log in, add, view, filter, calculate totals, and delete expenses with an intuitive dashboard interface.

---

## Features

### Core Functionality
* ✅ **User Authentication** - Register, login, and logout with secure password hashing
* ✅ **Password Recovery** - Forgot password with OTP verification via email
* ✅ **Change Password** - Change password while logged in
* ✅ **Add Expenses** - Add new expenses with description, amount, category, and date
* ✅ **View Expenses** - Display all expenses in a sorted list
* ✅ **Filter Expenses** - Filter by category, date range (start and end date)
* ✅ **Edit Expenses** - Update existing expense details
* ✅ **Delete Expenses** - Remove expenses with confirmation
* ✅ **Expense Analytics** - View expense summary metrics:
  - Total expenses (overall)
  - Today's expenses
  - Current month expenses
  - Expenses by category (breakdown)
  - Daily expense totals
* ✅ **Account Management** - View and manage user account details
* ✅ **Input Validation** - Comprehensive form validation with error handling
* ✅ **Email Notifications** - Send password reset codes via Gmail SMTP
* ✅ **Session Management** - Secure user sessions with login decorators

---

## Tech Stack

### Backend
* **Python 3.12**
* **Flask** - Web framework
* **Flask-SQLAlchemy** - ORM for database operations
* **Flask-Mail** - Email notifications
* **Werkzeug** - Security utilities (password hashing)
* **python-dotenv** - Environment variable management

### Database
* **SQLite** - Local database

### Frontend
* **HTML5** - Markup
* **Tailwind CSS** - Styling and responsive design
* **Jinja2** - Template engine

### Deployment
* **Docker** - Containerization
* **Azure App Service** - Cloud deployment
* **Azure Container Registry** - Image storage

---

## Project Structure

```text
Expense_Tracker/
│
├── README.md                    # Project documentation
├── DOCUMENTATION.md             # Detailed technical documentation
├── AI_NOTES.md                  # AI usage notes
├── Dockerfile                   # Docker configuration
├── requirements.txt             # Python dependencies
├── app.py                        # Main Flask application
│
├── templates/                   # HTML templates
│   ├── base.html               # Base template with navbar
│   ├── index.html              # Dashboard
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── forgot_password.html    # Password recovery
│   ├── verify_otp.html         # OTP verification
│   ├── change_password.html    # Change password
│   ├── edit.html               # Edit expense
│   ├── account.html            # Account settings
│   └── reset_password.html     # Reset password page
│
└── instance/                    # Instance folder
    └── expenses.db             # SQLite database (auto-created)
```

---

## Installation

### Prerequisites
* Python 3.12 or higher
* pip (Python package manager)
* Gmail account (for email functionality)

### Local Setup

1. **Clone the repository:**
```bash
git clone <YOUR_GITHUB_REPOSITORY_LINK>
cd Expense_Tracker
```

2. **Create a virtual environment:**
```bash
python -m venv .venv
```

3. **Activate virtual environment:**
   - **Windows:**
   ```bash
   .venv\Scripts\activate
   ```
   - **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Create `.env` file:**
Create a `.env` file in the root directory with the following variables:
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///expenses.db
```

> **Note:** For Gmail, generate an [App Password](https://support.google.com/accounts/answer/185833) instead of using your regular password.

---

## Running the Application

### Local Development
```bash
python app.py
```

The application will start on:
```text
http://localhost:4848
```

### Docker Deployment
```bash
docker build -t spendiq .
docker run -p 4848:4848 --env-file .env spendiq
```

---

## Azure Deployment

This application can be deployed to Azure App Service. See [Deployment Guide](#deployment-flow) for step-by-step instructions.

---

## Routes Overview

### Authentication Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |
| `/forgot-password` | GET, POST | Initiate password recovery |
| `/verify-otp` | GET, POST | Verify OTP for password reset |

### Expense Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Dashboard with expense summary |
| `/add` | POST | Add new expense |
| `/edit/<id>` | GET, POST | Edit existing expense |
| `/delete/<id>` | POST | Delete expense |

### Account Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/account` | GET | View account details |
| `/change-password` | GET, POST | Change password |

---

## Database Schema

### User Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | User's full name |
| email | String | Unique email address |
| password_hash | String | Hashed password |

### Expense Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| description | String | Expense description |
| amount | Float | Expense amount |
| category | String | Category (Food, Transport, Rent, etc.) |
| date | Date | Expense date |
| user_id | Integer | Foreign key (User) |

### PasswordResetOTP Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key (User) |
| otp_hash | String | Hashed OTP |
| expires_at | DateTime | OTP expiration time |
| attempts | Integer | Failed attempt count (max 5) |
| used | Boolean | Whether OTP has been used |
| created_at | DateTime | Creation timestamp |

---

## Environment Variables

Configure the following in your `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `MAIL_USERNAME` | Gmail address for sending emails | `your-email@gmail.com` |
| `MAIL_PASSWORD` | Gmail app password | `xxxx xxxx xxxx xxxx` |
| `SECRET_KEY` | Flask session secret key | `your-secret-key-here` |
| `PORT` | Application port (optional) | `4848` |

---

## Deployment Flow

This project includes support for Azure deployment via Docker. See the attached diagram for the complete deployment flow:

**SpendIQ Deployment Flow (Flask on Azure):**
1. Project (Flask App)
2. Docker File
3. Build Docker Image
4. Test Locally
5. Push Image to Azure Container Registry (ACR)
6. Create Azure App Service
7. Configure Settings & Environment Variables
8. Deploy & Access Live Application

---

## Security Features

* ✅ Password hashing with Werkzeug
* ✅ Secure session management
* ✅ OTP-based password recovery
* ✅ Rate limiting on OTP attempts (max 5)
* ✅ OTP expiration (10 minutes)
* ✅ User authentication decorators
* ✅ CSRF protection via Flask
* ✅ Input validation on all forms
* ✅ SQL injection prevention via SQLAlchemy ORM

---

## Error Handling

The application includes comprehensive error handling:
* Form validation with user-friendly error messages
* Flash messages for user feedback
* Database error management
* Email sending failure handling
* Session timeout management

---

## Future Enhancements

* 📊 Advanced expense analytics and charts
* 📱 Mobile app
* 💰 Budget tracking and alerts
* 📊 Expense comparison (monthly/yearly)
* 🔔 Notification system
* 📧 Email reports
* 👥 Family expense sharing
* 🎯 Savings goals tracking

---

## API Endpoints Reference

### Add Expense

**POST** `/add`

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
