from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from app.config.config import settings
from app.core.models.models import Base

engine: Engine = create_engine(
    url=settings.DB_URL,
    echo=True
)


@event.listens_for(Engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_and_tables() -> None:
    Base.metadata.create_all(bind=engine)


SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
