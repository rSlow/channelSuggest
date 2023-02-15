from sqlalchemy import select, ForeignKey, update
from sqlalchemy.orm import Mapped, mapped_column
from ORM.base import Base, Session


class UserState(Base):
    __tablename__ = "user_states"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    state: Mapped[str] = mapped_column(nullable=True)

    @classmethod
    async def set_state(cls,
                        user_id: str | int,
                        state: bytes | str):
        async with Session() as session:
            async with session.begin():
                query = update(
                    cls
                ).filter_by(
                    user_id=user_id
                ).values(
                    state=state
                )
                await session.execute(query)

    @classmethod
    async def get_all_states(cls):
        async with Session() as session:
            async with session.begin():
                query = select(cls)
                result = await session.execute(query)
                users = result.scalars().all()
        return users
