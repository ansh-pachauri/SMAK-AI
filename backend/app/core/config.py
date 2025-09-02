from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "SMAK AI API"
    debug: bool = False
    version: str = "1.0.0"
    
    # Database settings (for future use)
    database_url: Optional[str] = None
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"


settings = Settings()
