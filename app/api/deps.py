from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


SessionDep: type[Session] = Annotated[Session, Depends(dependency=get_db)]
