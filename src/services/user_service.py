from sqlalchemy.orm import Session
from models.user_model import User
from schema.user_schema import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    hashed_password = user.password
    db_user = User(
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        pin=user.pin,
        password=hashed_password,
        country=user.country,
        address=user.address,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

def update_user(db: Session, db_user: User, user_update: UserUpdate):
    if user_update.password:
        db_user.password =user_update.password
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
