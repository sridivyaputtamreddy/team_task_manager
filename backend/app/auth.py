from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import hashlib

# ========================
# LOAD ENV VARIABLES
# ========================
load_dotenv()

# ========================
# JWT CONFIG
# ========================
SECRET_KEY = os.getenv(
    "JWT_SECRET",
    "my_super_secret_key_123456"
)

ALGORITHM = "HS256"

# ========================
# PASSWORD HASHING SETUP
# ========================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ========================
# PASSWORD SAFETY FIX
# (Fixes bcrypt 72-byte limit)
# ========================
def normalize_password(password: str) -> str:
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ========================
# HASH PASSWORD
# ========================
def hash_password(password: str) -> str:
    safe_password = normalize_password(password)
    return pwd_context.hash(safe_password)


# ========================
# VERIFY PASSWORD
# ========================
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    safe_password = normalize_password(
        plain_password
    )

    return pwd_context.verify(
        safe_password,
        hashed_password
    )


# ========================
# CREATE JWT TOKEN
# ========================
def create_access_token(
    data: dict,
    expires_hours: int = 24
) -> str:

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        hours=expires_hours
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )