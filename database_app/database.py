from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

Base = declarative_base()

engine = create_engine(settings.DATABASE_URI.unicode_string())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
