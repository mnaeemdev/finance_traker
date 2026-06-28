# Spec: Login and Logout

## Overview

This step completes the authentication flow by implementing the logout functionality. Step 2 established user registration and login, storing user session data in Flask's session object. This step adds a logout route that safely clears the session and redirects users back to the landing page, completing the user authentication loop for Spendly.

## Depends on

- **Step 1: Database Setup** — users table with id, name, email, password_hash
- **Step 2: Registration** — user registration and login routes, session management

## Routes

- `POST /logout` — clears user session and redirects to landing page — logged-in users only

## Database changes

No database changes.

## Templates

- **Modify:** `base.html` — update navbar to show "Sign out" link when user is logged in (session contains user_id)

## Files to change

- `app.py` — replace logout stub with functional logout route
- `templates/base.html` — add conditional logout link to navbar

## Files to create

None.

## New dependencies

No new dependencies.

## Rules for implementation

- Use Flask's `session.clear()` to remove all session data
- Logout should only be accessible to logged-in users (check `session.get('user_id')`)
- Redirect to landing page (`url_for('landing')`) after logout
- Flash a success message: "Logged out successfully"
- The navbar must show "Sign out" link only when user is logged in; hide "Sign in" and "Get started" links
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done

- [ ] User can click "Sign out" link in navbar when logged in
- [ ] Clicking "Sign out" clears the session and shows a success message
- [ ] User is redirected to landing page after logout
- [ ] Navbar shows "Sign in" and "Get started" links again after logout
- [ ] Session data (user_id, user_name) is completely cleared
- [ ] Accessing protected routes (e.g., profile, expenses) after logout shows login page or error
- [ ] CSRF protection is in place if needed for logout (POST method)
