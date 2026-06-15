import os
from datetime import datetime, timedelta
import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_COMPLEX_KEY_HERE_123!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Hashes a plain text password using native bcrypt."""
    # Convert string to bytes, generate salt, and hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # Return as string to store easily in PostgreSQL
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against the stored string hash safely."""
    try:
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False

def create_access_token(data: dict):
    """Generates a secure JWT token access keycard."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt