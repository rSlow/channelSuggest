from sqlalchemy import select, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm.base import Base, Session
from orm.posts import Post


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)
    dice: Mapped["Dice"] = relationship(back_populates="telegram_user")

    queue_posts: Mapped[list["Post"]] = relationship()

    @classmethod
    async def add(cls, user_id, username):
        async with Session() as session:
            async with session.begin():
                session.add(
                    cls(
                        telegram_id=user_id,
                        username=username,
                        dice=Dice()
                    )
                )

    @classmethod
    async def get_all(cls):
        async with Session() as session:
            async with session.begin():
                query = select(cls.telegram_id)
                result = await session.execute(query)
                users = result.scalars().all()
        return users


class Dice(Base):
    __tablename__ = "dice"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    telegram_user: Mapped["User"] = relationship(back_populates="dice")

    cube: Mapped[int] = mapped_column(default=0)
    darts: Mapped[int] = mapped_column(default=0)
    football: Mapped[int] = mapped_column(default=0)
    basketball: Mapped[int] = mapped_column(default=0)
    casino: Mapped[int] = mapped_column(default=0)

    @classmethod
    async def play_cube(cls, user_id):
        async with Session() as session:
            query = select(cls).filter_by(telegram_user_id=user_id)
            result = await session.execute(query)
            stats: cls = result.scalars().one()
            stats.cube += 1
            await session.commit()

    @classmethod
    async def play_darts(cls, user_id):
        async with Session() as session:
            query = select(cls).filter_by(telegram_user_id=user_id)
            result = await session.execute(query)
            stats: cls = result.scalars().one()
            stats.darts += 1
            await session.commit()

    @classmethod
    async def play_football(cls, user_id):
        async with Session() as session:
            query = select(cls).filter_by(telegram_user_id=user_id)
            result = await session.execute(query)
            stats: cls = result.scalars().one()
            stats.football += 1
            await session.commit()

    @classmethod
    async def play_basketball(cls, user_id):
        async with Session() as session:
            query = select(cls).filter_by(telegram_user_id=user_id)
            result = await session.execute(query)
            stats: cls = result.scalars().one()
            stats.basketball += 1
            await session.commit()

    @classmethod
    async def play_casino(cls, user_id):
        async with Session() as session:
            query = select(cls).filter_by(telegram_user_id=user_id)
            result = await session.execute(query)
            stats: cls = result.scalars().one()
            stats.casino += 1
            await session.commit()
