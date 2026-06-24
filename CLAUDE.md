# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** is a personal expense tracking web application built with Flask (Python). It's a learning/tutorial project with incremental implementation steps. The landing page features a redesigned hero section with a YouTube video modal, Terms and Conditions, and Privacy Policy pages.

## Technology Stack

- **Backend:** Flask 3.1.3 (Python)
- **Frontend:** Jinja2 templates, vanilla CSS, vanilla JavaScript
- **Database:** SQLite (not yet fully implemented in `database/db.py`)
- **Testing:** pytest 8.3.5, pytest-flask 1.3.0
- **Fonts:** DM Sans (body), DM Serif Display (headings) from Google Fonts

## Development Setup

### Running the Application

```bash
pip install -r requirements.txt
python app.py
```

The app runs on `http://localhost:5001` with Flask debug mode enabled (auto-reload).

### Running Tests

```bash
pytest
pytest -v  # verbose output
pytest <test_file>::<test_name>  # run single test
```

## Project Structure

```
expense-tracker/
├── app.py                  # Flask app with routes
├── requirements.txt        # Python dependencies
├── .env                    # Development environment variables
├── database/
│   ├── db.py              # SQLite setup (stub, not yet implemented)
│   └── __init__.py
├── templates/             # Jinja2 templates (extends base.html)
│   ├── base.html          # Master template with navbar, footer, CSS/JS links
│   ├── landing.html       # Homepage (redesigned hero, features, CTA sections)
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── terms.html         # Terms and Conditions (12 sections)
│   └── privacy.html       # Privacy Policy (11 sections)
├── static/
│   ├── css/style.css      # Complete design system + all styling
│   └── js/main.js         # Client-side functionality (modal, animations)
└── assets/
    └── hero.png           # Hero section design mockup
```

## Key Architecture Notes

### Flask Routes

All routes are in `app.py` and render templates from the `templates/` directory using Flask's `render_template()`. Routes are organized in sections with comments.

**Implemented vs stub routes**
Route	Status
    `GET /`	Implemented — renders landing.html
    `GET /register`	Implemented — renders register.html
    `GET /login`	Implemented — renders login.html
    `GET /logout`	Stub — Step 3
    `GET /profile`	Stub — Step 4
    `GET /expenses/add`	Stub — Step 7
    `GET /expenses/<id>/edit`	Stub — Step 8
    `GET /expenses/<id>/delete`	Stub — Step 9
**Do not implement a stub route unless the active task explicitly targets that step.**

**Placeholder routes** (students will implement):
- `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`

### Design System (CSS)

`static/css/style.css` contains the complete design system using CSS custom properties. Key variables:

```css
--ink: #1a1a1a;                    /* text color */
--paper: #fafafa;                  /* background */
--paper-card: #ffffff;             /* card backgrounds */
--accent: #2ecc71;                 /* primary green */
--accent-light: #d4edda;           /* light green */
--font-body: 'DM Sans', sans-serif;
--font-display: 'DM Serif Display', serif;
--max-width: 1280px;               /* content max-width */
```

**Responsive breakpoints:** 900px, 768px (mobile-first approach)

### Hero Section (Recent Redesign)

The landing page hero is center-aligned, SaaS-style:
- Announcement badge with green dot
- Two-line headline ("Track every rupee." + "Know where it goes." in green)
- Centered subheadline
- Two CTA buttons (styled as pills with rounded corners)
- Dashboard preview card with stat cards and spending bars
- Fade-up animations with staggered timing (0.1s increments)

The hero uses `data-animate="fade-up"` attributes on elements and applies CSS animations (`@keyframes fadeUpAnimation`). All animations and layout changes are in `style.css`.

### Video Modal

The "See how it works" button opens a modal with an embedded YouTube iframe. The modal:
- Opens on button click
- Closes on X button or clicking outside the modal
- Stops video playback when closed (by resetting iframe src)

Implementation in `landing.html` and `static/js/main.js`.

### Templates Structure

All templates extend `base.html`, which provides:
- Navigation bar (brand, Sign in, Get started links)
- Footer (brand, copy text, Terms/Privacy links)
- CSS and JavaScript includes
- `{% block content %}` for page-specific content

Use `{% block title %}` to set page-specific titles.

## Common Development Tasks

### Adding a New Page

1. Create `templates/<page>.html` extending base.html
2. Add route in `app.py`: `@app.route("/<page>") def <page>(): return render_template("<page>.html")`
3. Update navbar/footer links in `base.html` if needed

### Styling

- Use CSS custom properties from the design system (e.g., `var(--accent)`, `var(--font-body)`)
- Keep media queries at the bottom of selectors or in a dedicated section
- For animations, use `@keyframes` and define timing in CSS (not inline styles)
- Ensure responsive design works at 900px and 768px breakpoints

### Adding JavaScript Functionality

- Keep client-side code in `static/js/main.js`
- Use vanilla JavaScript (no frameworks)
- Target elements by ID or class name
- Include comments for event listeners and modal logic

### Database Implementation

`database/db.py` is currently a stub. When implementing:
1. Import sqlite3
2. Implement `get_db()` — returns SQLite connection with row_factory and foreign keys enabled
3. Implement `init_db()` — creates all tables
4. Implement `seed_db()` — inserts sample data for development

## Warnings and things to avoid
1. Never use raw string returns for stub routes once a step is implemented — always render a template
2. Never hardcode URLs in templates — always use url_for()
3. Never put DB logic in route functions — it belongs in database/db.py
4. Never install new packages mid-feature without flagging it — keep requirements.txt in sync
5. Never use JS frameworks — the frontend is intentionally vanilla
database/db.py is currently empty — do not assume helpers exist until the step that implements them
6. FK enforcement is manual — SQLite foreign keys are off by default; get_db() must run PRAGMA foreign_keys = ON on every connection
7. The app runs on port 5001, not the Flask default 5001 — don't change this

## Environment Variables

`.env` contains:
- `FLASK_APP=app.py`
- `FLASK_ENV=development`
- `FLASK_DEBUG=True`
- `SECRET_KEY=dev-secret-key-change-in-production`
- `DATABASE_PATH=database/expenses.db`
- `PORT=5001`

## Git Workflow

The project uses GitHub for version control. Recent commits include landing page redesigns and compliance page additions. Commits are made with descriptive messages and changes are pushed to the main branch.
