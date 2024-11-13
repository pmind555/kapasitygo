# app/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CERT_API_KEY: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    LOG_LEVEL: str = "INFO"

    # Construct DATABASE_URL dynamically
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


    class Config:
        env_file = ".env.prod"

settings = Settings()
