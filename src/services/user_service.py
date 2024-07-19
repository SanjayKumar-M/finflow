from sqlalchemy.orm import Session
from models.user_model import User
from schema.user_schema import UserCreate, UserLogin
from nanoid import generate
import bcrypt
from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status

# You should store these securely, e.g., in environment variables
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

def create_user(db: Session, user: UserCreate):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
    
    db_user = User(
        user_id=generate(),
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        password=hashed_password.decode('utf-8'),
        country=user.country,
        account_no=user.account_no,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

def update_user_status(db: Session, user_id: str, new_status: str):
    user = get_user_by_id(db, user_id)
    if user:
        user.is_active = new_status
        db.commit()
        db.refresh(user)
        return user
    return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

def getProfile(db: Session):
    return db.query(User)