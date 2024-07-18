from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import declarative_base
from nanoid import generate
from datetime import datetime

Base = declarative_base()

def generate_id():
    return generate()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(21), primary_key=True, default=generate_id)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    account_no = Column(String, nullable=True)
    country = Column(String, nullable=False)
    is_active = Column(String, default="Update your KYC")
    amount = Column(Integer, server_default='100000')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
