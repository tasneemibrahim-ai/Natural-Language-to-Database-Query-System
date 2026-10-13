import sqlite3

conn = sqlite3.connect("data/sample.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE customers (id INTEGER, name TEXT, city TEXT)")
cursor.execute("CREATE TABLE orders (id INTEGER, customer_id INTEGER, amount REAL)")

cursor.execute("INSERT INTO customers VALUES (1, 'Ali', 'Cairo')")
cursor.execute("INSERT INTO customers VALUES (2, 'Sara', 'Alex')")

cursor.execute("INSERT INTO orders VALUES (1, 1, 500)")
cursor.execute("INSERT INTO orders VALUES (2, 2, 300)")

conn.commit()
conn.close()

print("✅ Database created successfully!")
print("   - customers table: 2 records")
print("   - orders table: 2 records")
