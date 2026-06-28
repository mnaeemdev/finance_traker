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
