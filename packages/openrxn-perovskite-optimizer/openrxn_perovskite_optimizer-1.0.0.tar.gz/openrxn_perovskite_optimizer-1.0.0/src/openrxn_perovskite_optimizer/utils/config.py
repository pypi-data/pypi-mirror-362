from pydantic_settings import BaseSettings
from typing import Optional

class DatabaseConfig(BaseSettings):
    url: str = "sqlite:///./test.db"

class LoggingConfig(BaseSettings):
    level: str = "INFO"
    file_path: Optional[str] = None

class Config(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    logging: LoggingConfig = LoggingConfig()

def load_config(path: Optional[str] = None) -> Config:
    if path:
        return Config(_env_file=path)
    return Config()