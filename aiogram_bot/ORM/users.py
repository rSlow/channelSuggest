from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ORM.base import Base, Session
from ORM.dice import Dice
from ORM.posts import Post
from ORM.states import UserState


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)

    dice: Mapped["Dice"] = relationship()
    state: Mapped["UserState"] = relationship()

    queue_posts: Mapped[list["Post"]] = relationship()

    @classmethod
    async def add(cls, user_id, username):
        async with Session() as session:
            async with session.begin():
                session.add(
                    cls(
                        telegram_id=user_id,
                        username=username,
                        dice=Dice(),
                        state=UserState()
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

