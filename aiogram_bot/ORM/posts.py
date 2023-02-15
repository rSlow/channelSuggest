import enum

from aiogram.types import ContentType
from sqlalchemy import ForeignKey, select, func, delete, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import mapped_column, Mapped, relationship, selectinload, immediateload

from ORM.base import Base, Session


class MediaTypes(enum.Enum):
    audio = ContentType.AUDIO
    video = ContentType.VIDEO
    document = ContentType.DOCUMENT
    photo = ContentType.PHOTO
    text = ContentType.TEXT


MediaTypesList = [i.value for i in MediaTypes]


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    user = relationship("User", back_populates="queue_posts")

    text: Mapped[str] = mapped_column(nullable=True)
    medias: Mapped[list["Media"]] = relationship(
        cascade="all, delete, delete-orphan"
    )

    async def add(self):
        async with Session() as session:
            async with session.begin():
                session.add(self)

    @classmethod
    async def get_user_post(cls, user_id: int, post_number: int):
        async with Session() as session:
            query = select(
                cls
            ).filter_by(
                user_id=user_id
            ).options(
                selectinload(cls.medias)
            ).offset(
                post_number - 1
            ).limit(1)
            result = await session.execute(query)
            post: cls = result.scalars().one()
        return post

    @classmethod
    async def get_user_posts_quantity(cls, user_id: int):
        async with Session() as session:
            query = select(
                func.count()
            ).select_from(
                cls
            ).filter_by(
                user_id=user_id
            )
            result = await session.execute(query)
            try:
                posts_quantity = result.scalars().one()
            except NoResultFound:
                posts_quantity = 0
        return posts_quantity

    @classmethod
    async def delete(cls, post):
        async with Session() as session:
            async with session.begin():
                query = delete(cls).filter_by(id=post.id)
                await session.execute(query)

    @classmethod
    async def get_all(cls, post_number: int):
        async with Session() as session:
            query = select(
                cls
            ).options(
                selectinload(cls.medias)
            ).options(
                selectinload(cls.user)
            ).offset(
                post_number - 1
            ).limit(1)
            result = await session.execute(query)
            post: cls = result.scalars().one()
        return post

    @classmethod
    async def get_all_quantity(cls):
        async with Session() as session:
            query = select(
                func.count()
            ).select_from(
                cls
            )
            result = await session.execute(query)
            try:
                posts_quantity = result.scalars().one()
            except NoResultFound:
                posts_quantity = 0
        return posts_quantity

    async def set_text(self, text: str):
        async with Session() as session:
            async with session.begin():
                query = update(
                    type(self)
                ).filter_by(
                    id=self.id
                ).values(
                    text=text
                )
                await session.execute(query)


class Media(Base):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    file_id: Mapped[str]
    media_type: Mapped["MediaTypes"]
