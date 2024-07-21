from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TWILIO_ACCOUNT_SID : str
    TWILIO_AUTH_TOKEN : str
    TWILIO_PHONE_NUMBER : str

    EMAIL_ADDRESS : str
    EMAIL_PASSWORD : str

    class Config:
        env_file = ".env"

settings = Settings()
