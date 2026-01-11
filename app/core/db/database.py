from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from app.config.config import settings
from app.core.models import Base

engine: Engine = create_engine(
    url=settings.DB_URL,
    echo=True
)


def create_db_and_tables() -> None:
    Base.metadata.create_all(bind=engine)


SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
