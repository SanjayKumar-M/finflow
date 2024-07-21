from sqlalchemy import Column, String, Boolean
from db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    mobile = Column(String)
    password = Column(String)
    country = Column(String)
    account_no = Column(String)
    is_active = Column(String)
    otp = Column(String, nullable=True)
    pin = Column(String, nullable=True)
    upi_id = Column(String, nullable=True)