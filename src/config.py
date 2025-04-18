from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GROK_API_KEY: str
    GROK_API_URL: str
    ALLOWED_ORIGINS: str

    class Config:
        env_file = ".env"

settings = Settings()
