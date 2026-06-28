# Spec: Profile Page

## Overview
The profile page is a dashboard for logged-in users that displays account details, expense summaries, recent activity, and category spending. It should feel polished and modern with summary cards at the top and a split panel below showing recent transactions and a category breakdown.

## Depends on
- Step 1: Database setup (users and expenses tables)
- Step 2: User registration
- Step 3: Login and logout functionality

## Routes
- `GET /profile` — displays logged-in user's account info, summaries, recent transactions, and category spending — logged-in only

## Database changes
No new tables. Add helper functions in `database/db.py`:
- `get_user_by_id(user_id)` — fetch user profile details without password hash
- `get_expense_stats(user_id)` — fetch total transaction count, total amount spent, top category, and category breakdown
- `get_recent_expenses(user_id, limit=5)` — fetch the most recent expenses for the profile page

## Templates
- **Create:** `templates/profile.html` — profile dashboard page
- **Modify:** `templates/base.html` — add "Profile" link to navbar (visible only when logged in)

## Files to change
- `app.py` — implement `/profile` route to fetch user and expense data and render template
- `database/db.py` — add `get_user_by_id()`, `get_expense_stats()`, and `get_recent_expenses()` helper functions
- `templates/profile.html` — build profile dashboard layout
- `templates/base.html` — add profile nav link and maintain logged-in state
- `static/css/style.css` — add profile dashboard styling and responsive layout

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw parameterized queries only
- Parameterized queries only (use `?` placeholders)
- Passwords are never displayed or accessed on profile page
- Use CSS custom properties — never hardcode colors or font sizes
- All templates extend `base.html`
- Profile route must check `session['user_id']` and redirect to `/login` if not authenticated
- Display user name, email, and account created date in the header card
- Show top summary cards for:
  - Total spent
  - Total transactions
  - Top category
- Show a recent transactions table with Date, Description, Category, and Amount
- Show a category breakdown panel with count, amount, and progress bars
- Use the app's existing design system and responsive breakpoints at 900px and 768px

## Definition of done
- [ ] `GET /profile` requires login and redirects unauthenticated users to `/login`
- [ ] Profile page header shows user name, email, and account creation date
- [ ] Profile page shows total spent, transaction count, and top spending category in summary cards
- [ ] Profile page includes a Recent Transactions section with date, description, category, and amount
- [ ] Profile page includes a By Category breakdown with count, amount, and visual bars
- [ ] Navbar shows "Profile" link only when logged in and points to `/profile`
- [ ] CSS styling uses custom properties and is responsive at 900px and 768px
- [ ] All SQL queries are parameterized
