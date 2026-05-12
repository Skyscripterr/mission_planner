from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///./missions.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

session_factory = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
Base = declarative_base()