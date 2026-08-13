# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///data/semiconnect.db")
    
    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-this-in-production")
    JWT_EXPIRATION_HOURS: int = 24
    
    # Rate Limiting
    RATE_LIMIT_CALLS: int = int(os.getenv("RATE_LIMIT_CALLS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    
    # Search
    SEARCH_CACHE_TTL: int = 3600  # 1 hour
    MAX_SEARCH_RESULTS: int = 5
    
    # Features
    ENABLE_ANALYTICS: bool = True
    ENABLE_REPORTING: bool = True
    
    # Subscription Tiers
    SUBSCRIPTION_TIERS = {
        "free": {
            "name": "Free",
            "price": 0,
            "features": ["basic_search", "vlsi_tutor", "learning_path"],
            "limits": {"searches_per_day": 10}
        },
        "pro": {
            "name": "Pro",
            "price": 49,
            "features": ["advanced_analytics", "export_reports"],
            "limits": {"searches_per_day": 100}
        },
        "enterprise": {
            "name": "Enterprise",
            "price": 499,
            "features": ["all_pro_features", "custom_models", "api_access"],
            "limits": {"searches_per_day": 1000}
        }
    }

config = Config()
