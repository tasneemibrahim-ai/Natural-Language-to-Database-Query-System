import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.db")


def setup_database() -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            city TEXT
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            order_date TEXT DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'pending'
        );
    """)
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executescript("""
            INSERT INTO users (name, email, age, city) VALUES
                ('Alice Johnson', 'alice@example.com', 29, 'New York'),
                ('Bob Smith', 'bob@example.com', 34, 'Los Angeles'),
                ('Carol White', 'carol@example.com', 25, 'Chicago'),
                ('David Brown', 'david@example.com', 42, 'Houston'),
                ('Eve Davis', 'eve@example.com', 31, 'Phoenix');

            INSERT INTO products (name, category, price, stock) VALUES
                ('Laptop Pro', 'Electronics', 1299.99, 50),
                ('Wireless Mouse', 'Electronics', 29.99, 200),
                ('Desk Chair', 'Furniture', 349.99, 30),
                ('Notebook', 'Stationery', 4.99, 500),
                ('USB Hub', 'Electronics', 49.99, 150),
                ('Standing Desk', 'Furniture', 599.99, 20);

            INSERT INTO orders (user_id, product_id, quantity, total_price, order_date, status) VALUES
                (1, 1, 1, 1299.99, '2024-01-10', 'delivered'),
                (1, 2, 2, 59.98,   '2024-01-15', 'delivered'),
                (2, 3, 1, 349.99,  '2024-02-01', 'shipped'),
                (3, 4, 5, 24.95,   '2024-02-10', 'delivered'),
                (4, 5, 3, 149.97,  '2024-03-01', 'pending'),
                (5, 1, 1, 1299.99, '2024-03-05', 'delivered'),
                (2, 6, 1, 599.99,  '2024-03-10', 'shipped'),
                (3, 2, 1, 29.99,   '2024-03-12', 'pending');
        """)
    conn.commit()
    conn.close()
    return DB_PATH


def get_schema() -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    parts = []
    for table in tables:
        cur.execute(f"PRAGMA table_info({table})")
        cols = ", ".join(f"{c[1]} {c[2]}" for c in cur.fetchall())
        parts.append(f"Table: {table} ({cols})")
    conn.close()
    return "\n".join(parts)
