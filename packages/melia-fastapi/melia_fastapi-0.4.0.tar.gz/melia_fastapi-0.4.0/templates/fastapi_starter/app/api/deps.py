from functools import lru_cache
from app.core.settings import  Settings
from app.core.database import  get_db_session

@lru_cache()
def get_settings() -> Settings:
    return Settings()

@lru_cache()
def get_db():
    return get_db_session()