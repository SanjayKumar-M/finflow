from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from schema.user_schema import UserCreate, UserOut
from services.user_service import create_user, get_user_by_email, update_user_status
from models.user_model import Base

app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

@app.post("/api/v1/users/register", response_model=UserOut)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@app.put("/api/v1/users/{user_id}/status", response_model=UserOut)
async def change_status(user_id: str, status: str, db: Session = Depends(get_db)):
    updated_user = update_user_status(db, user_id, status)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.get("/")
def read_root():
    return {"message": "Welcome to FinFlow"}
