from fastapi import FastAPI
from db.database import engine
from models.user_model import Base
from api.v1 import users

app = FastAPI()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include the users router
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FinFlow"}