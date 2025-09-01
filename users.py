# Temporary in-memory user storage
# users_db = {}

# def get_user(email: str):
#     return users_db.get(email)

# def create_user(email: str, hashed_password: str):
#     users_db[email] = {
#         "email": email,
#         "hashed_password": hashed_password
#     }

from database import SessionLocal, User

def get_user(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    print(email)
    db.close()
    return user

def create_user(email: str, hashed_password: str):
    db = SessionLocal()
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.close()
