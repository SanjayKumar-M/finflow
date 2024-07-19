from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    mobile: str
    country: str
    account_no: str
    is_active: bool = True

class UserOut(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    mobile: str
    country: str
    account_no: str
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str