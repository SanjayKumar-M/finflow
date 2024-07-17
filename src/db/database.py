from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import settings
from sqlalchemy.orm import Session

engine = create_engine(settings.DATABASE_URL)

sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db: Session = sessionLocal()  # Create a new Session object
    try:
        yield db
    finally:
        db.close()  # Close the Session object
