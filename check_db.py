# check_db.py
import sqlite3

conn = sqlite3.connect('data/semiconnect.db')
cursor = conn.cursor()

# Check all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:", tables)

# Check users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("\nUsers found:", len(users))
for u in users:
    print(u)

conn.close()
