from fastapi import FastAPI, HTTPException, Depends, status , APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app_access = APIRouter()

# MongoDB setup
client = MongoClient("mongodb+srv://admin:Abcd@cluster0.2cjvxnm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["user_auth_system"]
users_collection = db["users"]

# Password hashing context setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 setup for token generation and authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserInDB(BaseModel):
    username: str
    hashed_password: str

class User(BaseModel):
    username: str
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return False
    if not pwd_context.verify(password, user["hashed_password"]):
        return False
    return user

@app_access.post("/users/register", status_code=status.HTTP_201_CREATED)
def register_user(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    user_dict = user.dict()
    user_dict.update({"hashed_password": hashed_password})
    del user_dict["password"]  # Remove plain password from the dict before storing
    users_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}

@app_access.post("/token", description="Login for registered users")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user["username"], "token_type": "bearer"}

@app_access.get("/users/me", description="Read users by token")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = users_collection.find_one({"username": token})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_access, host="127.0.0.1", port=8000)
