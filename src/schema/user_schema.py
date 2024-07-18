from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    country: str
    account_no: Optional[str] = None
    is_active: Optional[str] = "Update your KYC"

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    user_id: str
    amount: int
    created_at: datetime

    class Config:
        orm_mode = True
