from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile = Column(String, unique=True, nullable=False)
    pin = Column(Integer, nullable=False)
    password = Column(String, nullable=False)
    account_no = Column(String, nullable=False)  # Ensure this is not nullable
    country = Column(String, nullable=False)
    address = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
