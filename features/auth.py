# features/auth.py
import bcrypt
import streamlit as st
from database.models import User, Usage, get_db_connection
import os
from datetime import datetime, timedelta
import jwt

class AuthManager:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-this-in-production")
    
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, email: str, password: str, tier: str = "free") -> bool:
        if User.get_by_email(email):
            return False
        hashed = self.hash_password(password)
        return User.create(email, hashed, tier)
    
    def register_user(self, email: str, username: str, password: str):
        """Register a new user"""
        if User.get_by_email(email):
            return None
        hashed = self.hash_password(password)
        # Use email as username if not provided
        if not username:
            username = email
        return User.create(email, hashed, "free")
    
    def authenticate_user(self, email: str, password: str):
        user = User.get_by_email(email)
        if not user:
            return None
        
        if self.verify_password(password, user['password_hash']):
            conn = get_db_connection()
            conn.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE email = ?",
                (email,)
            )
            conn.commit()
            conn.close()
            return user
        return None
    
    def get_user_tier(self, email: str) -> str:
        user = User.get_by_email(email)
        return user['tier'] if user else "free"
    
    def get_daily_limit(self, email: str) -> int:
        tier = self.get_user_tier(email)
        limits = {
            "free": 10,
            "pro": 100,
            "enterprise": 1000
        }
        return limits.get(tier, 10)
    
    def check_usage_limit(self, email: str) -> bool:
        user = User.get_by_email(email)
        if not user:
            return False
        usage = Usage.get_today_usage(user['id'])
        limit = self.get_daily_limit(email)
        return usage['messages_used'] < limit
    
    def create_token(self, user_id, email):
        """Create JWT token"""
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    