from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
import hashlib

# ========================
# JWT CONFIG
# ========================
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

# ========================
# PASSWORD HASHING SETUP
# ========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ========================
# PASSWORD SAFETY FIX
# (Fixes bcrypt 72-byte limit issue)
# ========================
def normalize_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    safe_password = normalize_password(password)
    return pwd_context.hash(safe_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    safe_password = normalize_password(plain_password)
    return pwd_context.verify(safe_password, hashed_password)


# ========================
# JWT TOKEN GENERATION
# ========================
def create_access_token(data: dict, expires_hours: int = 24) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)