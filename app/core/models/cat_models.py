from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class SpyCatModel(Base):
    __tablename__: str = "spy_cats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    breed: Mapped[str]
    experience: Mapped[int]
    salary: Mapped[int]
    is_available: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"<SpyCat {self.name=} {self.breed=} {self.experience=} {self.salary=}>"
