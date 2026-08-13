# utils/security.py
import re
import secrets
import hashlib

class SecurityManager:
    def __init__(self):
        pass
    
    def validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_password(self, password: str) -> tuple:
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        return len(errors) == 0, errors
    
    def sanitize_input(self, text: str) -> str:
        text = re.sub(r'[<>/]', '', text)
        return text.strip()
    
    def hash_sensitive_data(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()
    
    def generate_secure_token(self) -> str:
        return secrets.token_hex(32)
    
    def mask_email(self, email: str) -> str:
        username, domain = email.split('@')
        if len(username) > 2:
            masked = username[0] + '*' * (len(username) - 2) + username[-1]
        else:
            masked = username
        return f"{masked}@{domain}"
    