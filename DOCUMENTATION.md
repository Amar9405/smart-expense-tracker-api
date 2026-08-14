# SpendIQ - Complete Technical Documentation

## Project Overview

**SpendIQ** is a full-featured expense tracking web application built with Flask and SQLAlchemy. It allows users to manage their personal finances by recording, categorizing, filtering, and analyzing expenses. The application features a secure authentication system with password recovery, email notifications, and a responsive dashboard for expense management.

This project demonstrates modern web development practices including:
* Secure user authentication with password hashing
* Email integration for password recovery
* OTP-based verification system
* RESTful routing patterns
* Database modeling with SQLAlchemy ORM
* Form validation and error handling
* Session management
* Responsive frontend with Tailwind CSS
* Docker containerization
* Cloud deployment on Azure

---

## Project Objectives

The main objectives of SpendIQ are:

1. **Provide a User-Friendly Expense Tracker** - Enable users to easily record and manage their expenses.
2. **Secure Authentication** - Implement secure user registration, login, and password recovery mechanisms.
3. **Expense Analytics** - Provide meaningful insights into spending patterns through categorization and totals.
4. **Scalable Architecture** - Build a maintainable, containerized application ready for cloud deployment.
5. **Professional UI/UX** - Create an intuitive and visually appealing dashboard with responsive design.
6. **Email Integration** - Send password recovery codes via email for enhanced security.
7. **Best Practices** - Demonstrate clean code, proper validation, and error handling.

---

## Architecture & Technology Stack

### Backend Architecture
```
User Request
    ↓
Flask Web Framework
    ↓
Route Handlers (app.py)
    ↓
SQLAlchemy ORM
    ↓
SQLite Database
```

### Technology Stack Details

**Backend Framework:**
- **Flask** - Lightweight WSGI web framework for Python
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-Mail** - Email sending functionality
- **Werkzeug** - Security utilities for password hashing
- **python-dotenv** - Environment variable management

**Database:**
- **SQLite** - Serverless, file-based SQL database
- **SQLAlchemy** - Python SQL toolkit and Object Relational Mapper

**Frontend:**
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework for responsive design
- **Jinja2** - Template engine for dynamic HTML rendering

**Infrastructure:**
- **Docker** - Containerization for consistent environments
- **Azure Container Registry** - Container image repository
- **Azure App Service** - Cloud hosting platform

**Development Tools:**
- **Python 3.12** - Programming language
- **Virtual Environment** - Isolated Python environment
- **Git** - Version control
- **GitHub** - Repository hosting

---

## Core Features & Implementation

### 1. User Authentication System

**Registration** (`/register`)
- Form validation (name, email, password)
- Password strength requirements (minimum 8 characters)
- Password confirmation matching
- Duplicate email checking
- Password hashing using werkzeug.security

**Login** (`/login`)
- Email and password validation
- Session creation upon successful login
- Invalid credential handling
- Guest-only decorator to prevent logged-in users from re-logging

**Logout** (`/logout`)
- Session clearing
- Redirect to login page

### 2. Password Recovery System

**Forgot Password** (`/forgot-password`)
- Email lookup in database
- OTP generation (6-digit random number)
- Email sending via Gmail SMTP
- Session storage of reset user ID
- OTP expiration set to 10 minutes

**OTP Verification** (`/verify-otp`)
- 6-digit OTP validation
- Attempt limiting (maximum 5 attempts)
- OTP expiration checking
- Hash-based OTP comparison
- Automatic login upon successful OTP verification

**Change Password** (`/change-password`)
- Current password verification
- New password strength validation
- Password confirmation matching
- Prevention of reusing current password
- Secure password hash update

### 3. Expense Management

**Add Expense** (`/add` - POST)
- Description input validation
- Amount validation (positive numbers only)
- Category selection from predefined list
- Date picker with default to today
- User association via session user_id
- Database insertion with error handling

**View Expenses** (`/` - GET)
- Authenticated user's expenses only
- Sorted by date (newest first)
- Dynamic category and date filtering
- Expense summary metrics:
  - Total expenses
  - Today's expenses
  - Current month expenses
  - Category breakdown
  - Daily totals

**Edit Expense** (`/edit/<id>` - GET/POST)
- Authorization check (user owns expense)
- Form pre-population with current values
- Same validation as add expense
- Database update with transaction

**Delete Expense** (`/delete/<id>` - POST)
- Authorization check
- Safe deletion with error handling
- Immediate redirect to dashboard

### 4. Account Management

**View Account** (`/account`)
- Display user profile information
- Show user email and name
- Link to change password

**Change Password** (`/change-password`)
- Separate route for password updates
- Current password verification before change
- New password validation

### 5. Email System

**Gmail SMTP Configuration**
- Host: smtp.gmail.com
- Port: 587 (TLS)
- Authentication via app-specific password
- Email template for OTP messages

**Email Features**
- Password reset code delivery
- Professional email formatting
- Personalized greeting with user name
- Clear expiration information

---

## Database Schema & Models

### User Model
```python
class User(db.Model):
    id              → Integer (Primary Key)
    name            → String(100) - User's full name
    email           → String(120) - Unique email address
    password_hash   → String(255) - Hashed password
    expenses        → Relationship to Expense
    password_reset_otps → Relationship to PasswordResetOTP
```

### Expense Model
```python
class Expense(db.Model):
    id              → Integer (Primary Key)
    description     → String(120) - Expense description
    amount          → Float - Expense amount
    category        → String(50) - Expense category
    date            → Date - Expense date (default: today)
    user_id         → Integer (Foreign Key → User)
    user            → Relationship to User
```

### PasswordResetOTP Model
```python
class PasswordResetOTP(db.Model):
    id              → Integer (Primary Key)
    user_id         → Integer (Foreign Key → User)
    otp_hash        → String(255) - Hashed OTP value
    expires_at      → DateTime - OTP expiration timestamp
    attempts        → Integer - Failed attempt counter
    used            → Boolean - OTP usage status
    created_at      → DateTime - Creation timestamp
    user            → Relationship to User
```

### Relationships
- **User ↔ Expense** - One user has many expenses (1:N)
- **User ↔ PasswordResetOTP** - One user has many OTPs (1:N)

---

## Route Handlers & Decorators

### Custom Decorators

**`@login_required`**
- Wraps routes requiring authentication
- Checks for user_id in session
- Redirects to login page if not authenticated
- Used on: `/`, `/add`, `/edit`, `/delete`, `/account`, `/change-password`

**`@guest_only`**
- Prevents logged-in users from accessing certain pages
- Redirects to dashboard if already logged in
- Used on: `/register`, `/login`, `/forgot-password`, `/verify-otp`

### Route Summary

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/` | GET | Required | Dashboard with expense summary |
| `/add` | POST | Required | Add new expense |
| `/edit/<id>` | GET, POST | Required | Edit expense |
| `/delete/<id>` | POST | Required | Delete expense |
| `/register` | GET, POST | Guest | User registration |
| `/login` | GET, POST | Guest | User login |
| `/logout` | GET | - | User logout |
| `/forgot-password` | GET, POST | Guest | Password recovery |
| `/verify-otp` | GET, POST | Guest | OTP verification |
| `/account` | GET | Required | Account management |
| `/change-password` | GET, POST | Required | Change password |

---

## Form Validation & Error Handling

### Validation Rules

**Registration Form**
- Name: Required, non-empty
- Email: Required, unique, valid format
- Password: Minimum 8 characters
- Confirm Password: Must match password

**Login Form**
- Email: Required
- Password: Required
- Validation: Check against database

**Expense Form**
- Description: Required, non-empty
- Amount: Required, positive number only
- Category: Required, predefined list
- Date: Optional, defaults to today

**Password Change**
- Current Password: Must match user's current hash
- New Password: Minimum 8 characters
- Confirm Password: Must match new password
- Cannot reuse current password

### Error Messages
- Flash messages displayed via Jinja2 templates
- Categorized as "success" or "error"
- User-friendly and descriptive
- Clear guidance for correction

---

## Session Management

### Session Variables
```
session["user_id"]       → Authenticated user's ID
session["user_name"]     → User's display name
session["user_email"]    → User's email address
session["reset_user_id"] → Temporary ID during password reset
session["otp_verified"]  → OTP verification status
```

### Security Features
- Session clearing on logout
- Session clearing before login
- Temporary session for password reset flow
- User ownership validation on sensitive operations

---

## Expense Analytics

### Metrics Calculated in Dashboard

1. **Total Expense** - Sum of all user's expenses
2. **Today's Expense** - Sum of expenses for current date
3. **Month Expense** - Sum of expenses in current month/year
4. **Category Totals** - Dictionary of category-wise totals
5. **Daily Totals** - Dictionary of date-wise totals

### Filtering Options
- **By Category** - Single category selection
- **By Date Range** - Start date to end date filtering
- **Combined Filters** - Category + date range

---

## File Structure

```text
Expense_Tracker/
├── app.py                      # Main Flask application (900+ lines)
│   ├── Imports & Configuration
│   ├── Database Models
│   │   ├── User
│   │   ├── Expense
│   │   └── PasswordResetOTP
│   ├── Decorators
│   │   ├── @login_required
│   │   └── @guest_only
│   ├── Routes
│   │   ├── Authentication
│   │   ├── Expense Management
│   │   └── Account Management
│   └── Server Configuration
│
├── templates/                  # HTML Templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Dashboard
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── forgot_password.html   # Password recovery
│   ├── verify_otp.html        # OTP verification
│   ├── change_password.html   # Password change
│   ├── edit.html              # Expense editor
│   ├── account.html           # Account settings
│   └── reset_password.html    # Password reset page
│
├── instance/                   # Instance folder
│   └── expenses.db            # SQLite database (auto-created)
│
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .env.example               # Environment variables template
├── README.md                  # User documentation
├── DOCUMENTATION.md           # Technical documentation
└── AI_NOTES.md               # AI usage and modifications
```

---

## Environment Configuration

### .env File Setup
```env
# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password  # Gmail app-specific password

# Flask Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///expenses.db

# Server Configuration
PORT=4848
```

### Email Setup (Gmail)
1. Enable 2-factor authentication on Gmail
2. Generate an app-specific password
3. Use this password in .env file
4. Sender email is same as MAIL_USERNAME

---

## Deployment & Infrastructure

### Docker Deployment
**Dockerfile Configuration:**
- Base Image: python:3.12
- Working Directory: /app
- Exposed Port: 4848
- Entry Point: python app.py

**Build & Run:**
```bash
docker build -t spendiq .
docker run -p 4848:4848 --env-file .env spendiq
```

### Azure Deployment
**Components:**
1. **Azure Container Registry (ACR)** - Store Docker images
2. **Azure App Service** - Host the application
3. **Environment Variables** - Configure in App Service settings
4. **Continuous Deployment** - Optional GitHub Actions integration

**Deployment Steps:**
1. Build Docker image locally
2. Push to Azure Container Registry
3. Create Azure App Service (Linux)
4. Configure container settings
5. Set environment variables in App Service
6. Deploy and monitor

---

## Security Implementation

### Authentication Security
- ✅ Password hashing with Werkzeug (`generate_password_hash`, `check_password_hash`)
- ✅ Session-based authentication
- ✅ User ownership validation on operations

### Password Recovery Security
- ✅ 6-digit OTP generation using `secrets` module
- ✅ OTP hashing before storage
- ✅ 10-minute expiration time
- ✅ Maximum 5 attempt limit
- ✅ OTP invalidation after use

### Data Protection
- ✅ SQLAlchemy ORM prevents SQL injection
- ✅ Input validation on all forms
- ✅ CSRF protection via Flask
- ✅ Secure session management

### Email Security
- ✅ Gmail app-specific passwords (not main password)
- ✅ TLS encryption for SMTP
- ✅ Secure message formatting

---

## Error Handling & Validation

### Input Validation Layers
1. **Frontend** - HTML5 validation
2. **Backend** - Form data validation
3. **Database** - Constraints and relationships

### Common Error Scenarios
- Missing required fields → Flash error message
- Invalid email format → Validation error
- Duplicate email → User already exists message
- Wrong password → Invalid credentials message
- Expired OTP → Request new code
- OTP attempts exceeded → Try again later

### Transaction Safety
- Database operations wrapped in try-except
- Automatic rollback on errors
- User-friendly error messages

---

## Dashboard Features

### Summary Cards
- Total Expense amount
- Today's Expense amount
- Current Month Expense amount
- Recent transactions list

### Filtering & Search
- Filter by category dropdown
- Date range picker (start and end date)
- Real-time filtering and recalculation
- Persist filter selections in UI

### Expense List
- Table with sortable columns
- Edit and delete buttons per expense
- Date formatting
- Category badges
- Amount display with currency symbol

### Analytics
- Category wise breakdown
- Daily expense totals
- Running calculation totals

---

## Performance Considerations

### Database Optimization
- Indexed foreign keys
- Efficient query filtering
- Single query per page load
- Lazy relationship loading

### Frontend Optimization
- Tailwind CSS minification via CDN
- Responsive design for all screen sizes
- Dark theme for eye comfort
- Minimal JavaScript

### Scalability
- Containerized for easy scaling
- Environment-based configuration
- Session management scalable to multiple instances

---

## Testing Recommendations

### Manual Testing
1. **Authentication Flow**
   - Register new user
   - Login with correct/incorrect credentials
   - Logout functionality
   - Forgot password flow

2. **Expense Management**
   - Add expense with various categories
   - Filter by category
   - Filter by date range
   - Edit expense
   - Delete expense

3. **Dashboard**
   - Verify total calculations
   - Check category totals
   - Validate daily totals
   - Test filtering combinations

4. **Security**
   - Try accessing protected routes without login
   - Verify user can only see own expenses
   - Test invalid data submission

### Automated Testing
- Unit tests for models
- Integration tests for routes
- Validation tests for forms

---

## Troubleshooting

### Common Issues

**Email not sending:**
- Verify Gmail app-specific password
- Check MAIL_USERNAME and MAIL_PASSWORD in .env
- Ensure 2-factor authentication is enabled on Gmail
- Check firewall/network for SMTP port 587

**Database errors:**
- Delete instance/expenses.db and restart
- Check file permissions
- Verify SQLite is working correctly

**Session issues:**
- Clear browser cookies
- Check SECRET_KEY is set in .env
- Verify session timeout settings

**Port already in use:**
- Change PORT in .env
- Kill existing process on port 4848

---

## Future Enhancement Ideas

1. **Advanced Analytics**
   - Expense trend charts
   - Monthly/yearly comparisons
   - Budget vs actual tracking

2. **Social Features**
   - Shared expense tracking with family/friends
   - Expense splitting

3. **Mobile Experience**
   - PWA support
   - Mobile app (React Native/Flutter)

4. **Automation**
   - Recurring expenses
   - Bill reminders
   - Export to CSV/PDF

5. **Integration**
   - Bank account integration
   - Payment gateway integration
   - Third-party analytics

6. **AI Features**
   - Automatic categorization
   - Spending predictions
   - Personalized recommendations

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-08 | Initial release with core features |

---

## Support & Contribution

For issues, feature requests, or contributions, please visit the GitHub repository.

---

## License

This project is available for educational and personal use.

---

## Acknowledgments

**AI Tools Used:**
- ChatGPT
- GitHub Copilot

**For:**
- HTML/Tailwind CSS frontend design
- Flask and SQLAlchemy debugging
- Form validation logic
- Azure deployment guidance

**Core Logic & Integration:** Manually implemented and tested

---

## Contact & Support

For questions or issues regarding SpendIQ, please refer to the README.md file or contact the development team.

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
