from sqlalchemy.orm import Session
from app.database import SessionLocal

# Dependency to get the database session
def get_db():
    db = SessionLocal()  # Creates a new session
    try:
        yield db
    finally:
        db.close()  # Ensure the session is closed when done
