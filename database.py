from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite (개발용)
SQLALCHEMY_DATABASE_URL = "sqlite:///./wevity.db"

# PostgreSQL 사용 시 (운영용)
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
