from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Mistral API
    MISTRAL_API_KEY: str = "mstrl_bjo7l3AvLSVsT2w42EvRs394UMcb4JsB_2hdwmd"
    MISTRAL_MODEL: str = "pixtral-12b"

    # Database - Default to SQLite for local dev, override with TiDB/MySQL on Render
    # TiDB format: mysql+pymysql://username:password@host:4000/database?ssl_verify_cert=true
    DATABASE_URL: str = "sqlite:///./db/hints.db"

    # Security
    SECRET_KEY: str = "hintai_secret_2024_tidb"
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
