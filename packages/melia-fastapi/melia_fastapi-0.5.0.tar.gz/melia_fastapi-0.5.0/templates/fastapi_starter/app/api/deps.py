
from functools import lru_cache
from app.core.settings import  Settings
from app.core.database import SessionLocal

@lru_cache()
def get_settings() -> Settings:
    return Settings()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()