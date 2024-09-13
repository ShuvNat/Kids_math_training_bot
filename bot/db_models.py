from datetime import date
from uuid import UUID

from sqlalchemy import BigInteger, Date, Integer, ForeignKey, String, Uuid, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created_at: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=func.now(),
    )


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    # created_at добавляется из Base

    def __repr__(self) -> str:
        if self.last_name is None:
            name = self.first_name
        else:
            name = f"{self.first_name} {self.last_name}"
        return f"[{self.telegram_id}] {name}"

    tasks: Mapped[list["Tasks"]] = relationship(back_populates="user")


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
    )
    scales_and_fruis: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    fruit_picking: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    linear_equasion: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    area_and_perimeter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mistakes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # created_at добавляется из Base

    def __repr__(self) -> str:
        count = (self.scales_and_fruis + self.fruit_picking + self.linear_equasion + self.area_and_perimeter)
        if count in (11, 12, 13, 14) or count % 10 in (0, 5, 6, 7, 8, 9):
            word = 'здадач'
        elif count % 10 == 1:
            word = 'задачу'
        else:
            word = 'задачи'
        return f'Решено {count} {word}'

    user: Mapped["User"] = relationship(back_populates="tasks")
