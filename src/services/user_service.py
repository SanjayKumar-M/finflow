from sqlalchemy.orm import Session
from models.user_model import User
from schema.user_schema import UserCreate
from nanoid import generate

def create_user(db: Session, user: UserCreate):
    hashed_password = user.password  # Here you should hash the password
    db_user = User(
        user_id=generate(),
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        password=hashed_password,
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
