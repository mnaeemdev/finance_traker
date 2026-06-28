import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DATABASE_PATH = Path(__file__).parent.parent / "spendly.db"


def get_db():
    """Returns a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Creates all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def create_user(name, email, password):
    """Create a new user with hashed password. Raises sqlite3.IntegrityError on duplicate email."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password))
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_user_by_id(user_id):
    """Fetch user by ID; returns Row or None."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, email, created_at FROM users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def get_expense_stats(user_id):
    """Get expense summary for a user: total count, total amount, breakdown by category, top category."""
    conn = get_db()
    cursor = conn.cursor()

    # Total count and amount
    cursor.execute(
        "SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    total_count, total_amount = row[0], row[1]

    # Category breakdown
    cursor.execute(
        """SELECT category, COUNT(*) as count, COALESCE(SUM(amount), 0) as amount
           FROM expenses WHERE user_id = ?
           GROUP BY category ORDER BY amount DESC""",
        (user_id,)
    )
    by_category = [dict(r) for r in cursor.fetchall()]

    # Top category (highest spending)
    top_category = by_category[0] if by_category else None

    conn.close()

    return {
        "total_count": total_count,
        "total_amount": total_amount,
        "top_category": top_category,
        "by_category": by_category
    }


def get_recent_expenses(user_id, limit=5):
    """Fetch the most recent expenses for the profile page."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date, description, category, amount FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?",
        (user_id, limit)
    )
    expenses = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return expenses


def seed_db():
    """Inserts sample data for development."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if data already exists to avoid duplicates
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insert demo user with hashed password
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123"))
    )
    user_id = cursor.lastrowid

    # Insert 8 sample expenses across all categories
    expenses = [
        (user_id, 45.50, "Food", "2026-06-01", "Grocery shopping"),
        (user_id, 25.00, "Transport", "2026-06-05", "Gas"),
        (user_id, 120.00, "Bills", "2026-06-08", "Electricity bill"),
        (user_id, 35.00, "Health", "2026-06-12", "Pharmacy"),
        (user_id, 15.00, "Entertainment", "2026-06-15", "Movie tickets"),
        (user_id, 60.00, "Shopping", "2026-06-18", "New shoes"),
        (user_id, 10.50, "Food", "2026-06-20", "Coffee"),
        (user_id, 8.00, "Other", "2026-06-22", "Misc expense"),
    ]

    for user_id_val, amount, category, date, description in expenses:
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (user_id_val, amount, category, date, description)
        )

    conn.commit()
    conn.close()
