import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TWO_CAPTCHA_API_KEY: str = os.getenv("TWO_CAPTCHA_API_KEY", "")
    PROXY_URL: Optional[str] = None
    HEADLESS: bool = False
    USER_DATA_DIR: str = "user_data"
    
    class Config:
        env_file = ".env"

settings = Settings()
