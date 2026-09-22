pip install fastapi uvicorn "passlib[bcrypt]" PyJWT

import os
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt

app = FastAPI(title="Auth Microservice")

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration (Store secrets in environment variables in production)
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Simulated user database (Passwords are pre-hashed with bcrypt)
# In production, query your database (e.g., PostgreSQL, MongoDB)
FAKE_USER_DB = {
    "user123": {
        "user_id": "user123",
        # Pre-hashed version of "SecretPassword123"
        "hashed_password": pwd_context.hash("SecretPassword123")
    }
}

# Request schema for mobile payload
class LoginRequest(BaseModel):
    user_id: str
    password: str

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/api/v1/auth/login")
def login(credentials: LoginRequest):
    # 1. Fetch user from database
    user = FAKE_USER_DB.get(credentials.user_id)

    # 2. Validate user existence and password match
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Generate JWT access token
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["user_id"]},
        expires_delta=token_expires
    )

    # 4. Return response to mobile client
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in_seconds": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


uvicorn main:app --reload --port 8000


# End of code file
