from sqlalchemy import create_engine, Column, String
# create_engine: This sets up a connection to your database.
# Column and String: Used to define fields in your database tables (like columns in an Excel sheet).
from sqlalchemy.ext.declarative import declarative_base
# declarative_base(): This is the base class for all your models (i.e. tables).
# When you define a model (like User), it must inherit from this base.
from sqlalchemy.orm import sessionmaker
# sessionmaker: Used to create a "session" — which is how we talk to the database (read/write data).


# SQLite URL
DATABASE_URL = "sqlite:///./users.db"
# This is the connection string
# sqlite:///./users.db means:
# Use SQLite.
# Save the database file locally in the same folder as users.db.
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# engine is the "motor" that drives database connections.
# check_same_thread=False is needed for SQLite + FastAPI, to allow async behavior.


# 2. Create the engine (connects SQLAlchemy to your DB)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# This creates a database session factory.
# autocommit=False: Changes aren’t saved until .commit() is called.
# autoflush=False: Prevents automatic syncing between session and database.
# bind=engine: Ties this session to our SQLite engine.

Base = declarative_base()
# This defines the base class for all your table models.
# When you define a model (e.g., User), it will extend this.

# User model
class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)

# | Line                               | Purpose                                                     |
# | ---------------------------------- | ----------------------------------------------------------- |
# | `class User(Base)`                 | Defines a table called `User`                               |
# | `__tablename__ = "users"`          | Tells SQLAlchemy to name this table `users` in the DB       |
# | `email = Column(...)`              | Creates a column for storing email addresses                |
# | `primary_key=True`                 | Makes `email` the unique ID (i.e., no duplicates allowed)   |
# | `index=True`                       | Speeds up queries by creating an index on the `email` field |
# | `hashed_password = Column(String)` | Stores the user's hashed password                           |


# Create tables
Base.metadata.create_all(bind=engine)
# This line tells SQLAlchemy to create the actual tables in the database if they don’t already exist.
# Think of it as: "Build the table layout in users.db."


# Summary: database.py
# │
# ├── create_engine → connects to SQLite
# ├── SessionLocal → handles sessions
# ├── Base → base class for models
# ├── User → table definition
# └── create_all() → creates table if not exists
# pip install sqlalchemy

