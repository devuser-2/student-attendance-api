from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ DO NOT hash here
fake_user = {
    "username": "admin",
    "password": "admin123"
}

def verify_password(plain_password, stored_password):
    return plain_password == stored_password

def authenticate_user(username, password):
    if username != fake_user["username"]:
        return False
    if password != fake_user["password"]:
        return False
    return True

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)