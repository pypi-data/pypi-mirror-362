from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import Settings

settings = Settings()
db_settings = settings.db
DATABASE_URL = f"postgresql://{db_settings.user}:{db_settings.password}@{db_settings.host}:5432/{db_settings.database}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
