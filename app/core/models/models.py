from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class MissionModel(Base):
    __tablename__: str = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_completed: Mapped[bool] = mapped_column(default=False)
    assigned_cat_id: Mapped[int | None] = mapped_column(ForeignKey("spy_cats.id"))

    assigned_spy_cat: Mapped["SpyCatModel"] = relationship(back_populates="mission", single_parent=True)
    targets: Mapped[list["TargetModel"]] = relationship(
        back_populates="mission",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return (f"<Mission {self.id=} {self.is_completed=} "
                f"{self.assigned_spy_cat=} {self.targets=}>")


class TargetModel(Base):
    __tablename__: str = "targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    country: Mapped[str]
    notes: Mapped[str | None]
    is_completed: Mapped[bool] = mapped_column(default=False)
    mission_id: Mapped[int] = mapped_column(ForeignKey(column="missions.id", ondelete="CASCADE"))

    mission: Mapped[MissionModel] = relationship(back_populates="targets")

    def __repr__(self):
        return (f"\n <Target {self.id=} {self.mission_id=} {self.name=} {self.country=} "
                f"{self.is_completed=} {self.notes=} >")


class SpyCatModel(Base):
    __tablename__: str = "spy_cats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    breed: Mapped[str]
    experience: Mapped[int]
    salary: Mapped[int]
    is_available: Mapped[bool] = mapped_column(default=True)

    mission: Mapped[MissionModel | None] = relationship(back_populates="assigned_spy_cat")

    def __repr__(self) -> str:
        return f"<SpyCat {self.id=} {self.name=} {self.breed=} {self.experience=} {self.salary=}>"
