#prevent hackers from seeing anyone's real password:
# we are using securng Algorithm-> bcrypt
#pip install passlib[bcrypt]

from passlib.context import CryptContext

# Create a password context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Hash a password (during signup)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#This checks if the password the user typed matches the hashed version in the database
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

