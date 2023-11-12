import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    IFS_DB_URL:str
    IFS_JWT_SECRET_KEY:str
    IFS_JWT_ALGORITHM:str
    ChatGPT_API_KEY:str
    class Config:
        env_file = ".env"

settings = Settings()
