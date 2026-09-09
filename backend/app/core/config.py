from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Mistral API
    MISTRAL_API_KEY: str = "your_mistral_api_key"
    MISTRAL_MODEL: str = "pixtral-12b"

    # Database
    DATABASE_URL: str = "sqlite:///./db/hints.db"

    # Security
    SECRET_KEY: str = "change_this_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Mobile Money
    TMONEY_API_KEY: str = ""
    MOMO_API_KEY: str = ""

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
