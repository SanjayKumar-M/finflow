from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    pin: int
    country: str
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    user_id: str
    account_no: str
    is_active: bool
    amount: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    amount: Optional[int] = None
