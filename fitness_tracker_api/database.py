import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL or "postgresql" not in DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fitness_db"

print(f"🔌 API connecting directly to database URL: {DATABASE_URL}")


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    """Dependency to provide a database session to our FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()