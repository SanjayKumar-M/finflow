from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=8)
    mobile: str
    country: str
    account_no: str
    kyc_status: str = "KYC not updated"

    @validator('password')
    def password_complexity(cls, v):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', v):
            raise ValueError('Password must be at least 8 characters long and contain both letters and numbers')
        return v

    @validator('mobile')
    def mobile_format(cls, v):
        if not re.match(r'^\+?1?\d{9,15}$', v):
            raise ValueError('Invalid mobile number format')
        return v

class UserOut(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    mobile: str
    country: str
    account_no: str
    kyc_status: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str