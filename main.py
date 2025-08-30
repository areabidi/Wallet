# FastAPI()	Creates your app — like starting a blank website
# OAuth2PasswordBearer	Tells FastAPI how users will send their token
# Depends(...)	Lets FastAPI handle "middleware" logic like auth
# pydantic.BaseModel	Helps define and validate data from users


from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from auth import create_access_token, verify_token
from utils import hash_password, verify_password
from users import get_user, create_user


from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
#a fake database. Later, we’ll connect a real DB like PostgreSQL or SQLite.
fake_users_db = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User	Represents what users send to the API (plain password)
# UserInDB	Simulates what's stored in the database (hashed password)
class User(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(user: User):
    print("Signup received:", user)
    if get_user(user.email):
        print("User already exists:", user.email)
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hash_password(user.password)
    print("Hashed password:", hashed)
    create_user(user.email, hashed)
    return {"message": "User created successfully"}

@app.post("/login")
def login(user: User):
    db_user = get_user(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


# FastAPI automatically extracts the token from the request
# verify_token() checks if it’s valid
# If valid → returns a message
# If not → raises a 401 Unauthorized erro
@app.get("/protected")
def protected_route(token: str):
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": f"Welcome {email}, you are authenticated."}
