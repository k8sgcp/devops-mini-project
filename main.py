pip install fastapi uvicorn passlib[bcrypt] pyjwt

import datetime
from fastapi import FastAPI, HTTPException, Status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import jwt

app = FastAPI()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your_secret_key_change_in_production"
ALGORITHM = "HS256"

# In-memory user database (replace with PostgreSQL/MongoDB in production)
users_db = {}

# Pydantic schemas for Android JSON requests
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Helper functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Endpoints for Android ---

@app.post("/register", status_code=Status.HTTP_201_CREATED)
def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(
            status_code=Status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )
    
    # Store hashed password, never plain text
    users_db[user.email] = hash_password(user.password)
    return {"message": "Account created successfully."}

@app.post("/login")
def login(user: UserLogin):
    stored_hash = users_db.get(user.email)
    
    # Validate credentials
    if not stored_hash or not verify_password(user.password, stored_hash):
        raise HTTPException(
            status_code=Status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
    
    # Generate JWT for Android app
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


uvicorn main:app --reload --host 0.0.0.0 --port 8000
