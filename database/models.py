# database/models.py
import sqlite3
from datetime import datetime
from typing import Optional, Dict, List
import os

DB_PATH = "data/semiconnect.db"

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with all tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            tier TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Chat history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mode TEXT,
            message TEXT,
            role TEXT,
            response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Watchlist table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            company_name TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Usage tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date DATE,
            messages_used INTEGER DEFAULT 0,
            searches_used INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

class User:
    @staticmethod
    def create(email: str, password_hash: str, tier: str = "free") -> bool:
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (email, password_hash, tier) VALUES (?, ?, ?)",
                (email, password_hash, tier)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def update_tier(email: str, new_tier: str):
        conn = get_db_connection()
        conn.execute(
            "UPDATE users SET tier = ? WHERE email = ?",
            (new_tier, email)
        )
        conn.commit()
        conn.close()

class ChatHistory:
    @staticmethod
    def save(user_id: int, mode: str, message: str, role: str, response: str):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO chat_history (user_id, mode, message, role, response) VALUES (?, ?, ?, ?, ?)",
            (user_id, mode, message, role, response)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_history(user_id: int, limit: int = 50) -> List[Dict]:
        conn = get_db_connection()
        history = conn.execute(
            "SELECT * FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
        conn.close()
        return [dict(row) for row in history]

class Watchlist:
    @staticmethod
    def add(user_id: int, company_name: str):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO watchlist (user_id, company_name) VALUES (?, ?)",
            (user_id, company_name)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all(user_id: int) -> List[Dict]:
        conn = get_db_connection()
        companies = conn.execute(
            "SELECT * FROM watchlist WHERE user_id = ? ORDER BY added_at DESC",
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in companies]
    
    @staticmethod
    def remove(user_id: int, company_id: int):
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM watchlist WHERE user_id = ? AND id = ?",
            (user_id, company_id)
        )
        conn.commit()
        conn.close()

class Usage:
    @staticmethod
    def get_today_usage(user_id: int) -> Dict:
        conn = get_db_connection()
        today = datetime.now().date().isoformat()
        usage = conn.execute(
            "SELECT messages_used, searches_used FROM usage WHERE user_id = ? AND date = ?",
            (user_id, today)
        ).fetchone()
        conn.close()
        return dict(usage) if usage else {"messages_used": 0, "searches_used": 0}
    
    @staticmethod
    def increment(user_id: int, type: str):
        conn = get_db_connection()
        today = datetime.now().date().isoformat()
        
        existing = conn.execute(
            "SELECT id FROM usage WHERE user_id = ? AND date = ?",
            (user_id, today)
        ).fetchone()
        
        if existing:
            if type == "message":
                conn.execute(
                    "UPDATE usage SET messages_used = messages_used + 1 WHERE user_id = ? AND date = ?",
                    (user_id, today)
                )
            else:
                conn.execute(
                    "UPDATE usage SET searches_used = searches_used + 1 WHERE user_id = ? AND date = ?",
                    (user_id, today)
                )
        else:
            conn.execute(
                "INSERT INTO usage (user_id, date, messages_used, searches_used) VALUES (?, ?, ?, ?)",
                (user_id, today, 1 if type == "message" else 0, 1 if type == "search" else 0)
            )
        
        conn.commit()
        conn.close()
        