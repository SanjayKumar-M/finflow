from fastapi import FastAPI
from api.v1 import users
from db.database import Base, engine
from dotenv import load_dotenv
# Create all tables in the database

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(users.router)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FinFlow API Lite"}
