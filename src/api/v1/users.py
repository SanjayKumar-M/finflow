from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schema.user_schema import UserCreate, UserOut, UserLogin, Token
from services.user_service import create_user, get_user_by_email, login
from db.database import get_db
from core.security import oauth2_scheme
from jose import JWTError, jwt
from core.security import SECRET_KEY, ALGORITHM

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return create_user(db, user)

@router.post("/login", response_model=Token)
def login_for_access_token(user_login: UserLogin, db: Session = Depends(get_db)):
    return login(db, user_login)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

@router.get("/profile", response_model=UserOut)
async def read_users_profile(current_user: UserOut = Depends(get_current_user)):
    return current_user