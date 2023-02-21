from sqlalchemy import select, ForeignKey, update
from sqlalchemy.orm import Mapped, mapped_column
from ORM.base import Base, Session


class Dice(Base):
    __tablename__ = "dice"
    GAMES = [
        "cube",
        "darts",
        "football",
        "basketball",
        "casino"
    ]

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))

    cube: Mapped[int] = mapped_column(default=0)
    darts: Mapped[int] = mapped_column(default=0)
    football: Mapped[int] = mapped_column(default=0)
    basketball: Mapped[int] = mapped_column(default=0)
    casino: Mapped[int] = mapped_column(default=0)

    @classmethod
    async def _play_game(cls, user_id: int, game: str):
        if game not in cls.GAMES:
            raise TypeError(f"game {game} is not available")

        async with Session() as session:
            async with session.begin():
                game_subquery = select(cls.cube).filter_by(telegram_user_id=user_id).scalar_subquery()
                query = update(cls).filter_by(telegram_user_id=user_id).values(**{game: game_subquery + 1})
                await session.execute(query)

    @classmethod
    async def play_cube(cls, user_id: int):
        await cls._play_game(user_id=user_id, game="cube")

    @classmethod
    async def play_darts(cls, user_id: int):
        await cls._play_game(user_id=user_id, game="darts")

    @classmethod
    async def play_football(cls, user_id: int):
        await cls._play_game(user_id=user_id, game="football")

    @classmethod
    async def play_basketball(cls, user_id: int):
        await cls._play_game(user_id=user_id, game="basketball")

    @classmethod
    async def play_casino(cls, user_id: int):
        await cls._play_game(user_id=user_id, game="casino")
