# test_login.py
from database.models import init_database, get_db_connection
from features.auth import AuthManager

# Initialize database
init_database()

# Create auth manager
auth = AuthManager()

# Test credentials
email = "test@example.com"
password = "Test@123456"

print("=== TESTING LOGIN SYSTEM ===\n")

# Check if user exists
conn = get_db_connection()
user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
conn.close()

if user:
    print(f"✅ User exists: {email}")
    print(f"   Tier: {user['tier']}")
else:
    print("❌ User not found. Creating new user...")
    if auth.create_user(email, password):
        print("✅ User created successfully!")
    else:
        print("❌ Failed to create user")

# Try to authenticate
print("\n=== AUTHENTICATING ===\n")
result = auth.authenticate_user(email, password)
if result:
    print("✅ LOGIN SUCCESSFUL!")
    print(f"   User ID: {result['id']}")
    print(f"   Email: {result['email']}")
    print(f"   Tier: {result['tier']}")
else:
    print("❌ LOGIN FAILED!")
    print("   Invalid credentials")

print("\n=== ALL USERS ===\n")
conn = get_db_connection()
users = conn.execute("SELECT id, email, tier FROM users").fetchall()
conn.close()

for u in users:
    print(f"   ID: {u['id']}, Email: {u['email']}, Tier: {u['tier']}")
    