from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Ecom tech"
    debug: bool = False
    database_url: str

    class Config:
        env_file = ".env"