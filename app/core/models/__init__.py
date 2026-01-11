from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from .cat_models import SpyCatModel
