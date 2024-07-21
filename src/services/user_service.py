from sqlalchemy.orm import Session
from models.user_model import User
from schema.user_schema import UserCreate, UserLogin, OTPVerify, PinSet
from core.security import verify_password, get_password_hash, create_access_token
from fastapi import HTTPException, status
from nanoid import generate
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from config.config import settings

EMAIL_ADDRESS = settings.EMAIL_ADDRESS
EMAIL_PASSWORD = settings.EMAIL_PASSWORD

TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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
        is_active="Inactive",
        otp=generate_otp()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    send_otp(db_user.mobile, db_user.otp)
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

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp(phone_number: str, otp: str):
    message = twilio_client.messages.create(
        body=f'Hey User, Here is your OTP for KYC verification: {otp} Built by Sanjay',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

def verify_otp(db: Session, email: str, otp: OTPVerify):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.otp != otp.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    user.is_active = "Active"
    user.otp = None
    db.commit()
    send_activation_email(user.email,message="Account activated. Here are the next steps:\n1. SET pin\n2. Get your UPI ID and all set to make your first payment")
    return {"message": "KYC verification success"}

def send_activation_email(email: str,message: str):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Account Activated"

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS, email, text)
    server.quit()

def set_pin(db: Session, email: str, pin: PinSet):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.pin = get_password_hash(pin.pin)
    user.upi_id = f"{email.split('@')[0]}@finflow"
    db.commit()
    send_activation_email(user.email,message=f'You set your PIN, Here is your UPI ID: {user.upi_id}')
    return {"message": f"You set your pin successfully. Here is your UPI ID: {user.upi_id}"}