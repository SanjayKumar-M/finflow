from sqlalchemy.orm import Session
from models.user_model import User
from schema.user_schema import UserCreate, UserLogin
from core.security import verify_password, get_password_hash, create_access_token
from fastapi import HTTPException, status
from nanoid import generate

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        user_id=generate(),
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        password=hashed_password,
        country=user.country,
        account_no=user.account_no,
        kyc_status=user.kyc_status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def login(db: Session, user_login: UserLogin):
    user = authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}