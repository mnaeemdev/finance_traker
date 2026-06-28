# Spec: Registration

## Overview

Implement user registration functionality that allows new users to create accounts with their name, email, and password. This step establishes the foundation for user authentication, enabling users to sign up and store their credentials securely in the database. Registration is available without login and is the entry point for new users to access the Spendly expense tracker. After successful registration, users must log in with their credentials.

## Depends on

Step 1 — Database Setup. The `users` table and `get_db()` function must be fully implemented before building registration.

## Routes

- `GET /register` — Render registration form page — public access (no login required)
- `POST /register` — Accept registration form submission, validate input, create user in database, display success message, and redirect to login — public access (no login required)

## Database changes

No new tables. Add helper function `create_user(name, email, password)` to `database/db.py`:
- Accepts plain password and hashes it using `werkzeug.security.generate_password_hash`
- Inserts new row into `users` table with name, email, and password_hash
- Returns user ID on success
- Raises exception on email conflict (UNIQUE constraint violation)

## Form fields

Expect POST data with:
- `name` — User's full name (required, non-empty)
- `email` — Email address (required, valid email format)
- `password` — Password (required, minimum 8 characters)
- `password_confirm` — Password confirmation (required, must match password)

## Templates

- **Modify:** `templates/register.html`:
  - Add CSRF token to form (Flask requirement for POST)
  - Add password confirmation field (matches password validation)
  - Add flash message block to display errors and success messages
  - Wire form `action="{{ url_for('register') }}"` and `method="POST"`
  - Keep all existing visual design

## Files to change

- `app.py` — Implement `GET /register` (display form) and `POST /register` (process submission) routes
- `database/db.py` — Add `create_user()` helper function
- `templates/register.html` — Add CSRF token, password confirmation field, flash message block, and wire form action/method

## Files to create

None

## New dependencies

No new dependencies. Uses existing:
- `flask` (request handling)
- `werkzeug.security` (password hashing)
- `sqlite3` (database)

## Rules for implementation

- No SQLAlchemy or ORMs — use raw SQL with parameterized queries only
- All passwords must be hashed using `werkzeug.security.generate_password_hash()` before storing
- Never store plain text passwords
- Validate email format on the backend using regex (e.g., `r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'`)
- Validate password length (minimum 8 characters) on the backend
- Validate that password and password_confirm match — reject with "Passwords do not match" if different
- Handle UNIQUE constraint violations gracefully — display "Email already registered" without exposing SQL
- Use `url_for()` to generate URLs, never hardcode paths
- All templates extend `base.html`
- Use Flask `session` with `csrf_token` for CSRF protection, store in hidden form field
- Use Flask `flash()` to display success and error messages
- Success message on redirect: "Registration successful! Please log in with your credentials."

## Definition of done

- [ ] `GET /register` route renders registration form with CSRF token and password confirmation field
- [ ] `POST /register` route accepts form data (name, email, password, password_confirm)
- [ ] Form validates name is not empty
- [ ] Form validates email format using regex on backend
- [ ] Form validates password is at least 8 characters
- [ ] Form validates password and password_confirm match
- [ ] All validation errors are displayed on registration page with clear messages
- [ ] Error messages include: "Please enter a name", "Invalid email format", "Password must be at least 8 characters", "Passwords do not match", "Email already registered"
- [ ] Successful registration creates user in database with hashed password
- [ ] On successful registration, flash success message "Registration successful! Please log in with your credentials." and redirect to `/login`
- [ ] User must log in after registration (no auto-login)
- [ ] CSRF protection is enabled and validated on POST
- [ ] Password is never logged or displayed in error messages
- [ ] Form visual design and layout remains unchanged from original
