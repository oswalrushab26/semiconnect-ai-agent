# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///semiconnect.db")
    
    # Rate Limiting
    RATE_LIMIT_CALLS = int(os.getenv("RATE_LIMIT_CALLS", "10"))
    RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    
    # Tiers
    FREE_DAILY_LIMIT = 10
    PRO_DAILY_LIMIT = 100
    ENTERPRISE_DAILY_LIMIT = 1000

config = Config()
