import enum

from aiogram.types import ContentType
from sqlalchemy import ForeignKey, select, func, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import mapped_column, Mapped, relationship, selectinload

from ORM.base import Base, Session


class MediaTypes(enum.Enum):
    audio = ContentType.AUDIO
    video = ContentType.VIDEO
    document = ContentType.DOCUMENT
    photo = ContentType.PHOTO
    text = ContentType.TEXT


MediaTypesList = [i.value for i in MediaTypes]

media_annotations = {
    MediaTypes.audio.value: "аудио",
    MediaTypes.video.value: "видео",
    MediaTypes.document.value: "документ",
    MediaTypes.photo.value: "фото"
}


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    user = relationship("User", back_populates="queue_posts")

    text: Mapped[str] = mapped_column(nullable=True)
    medias: Mapped[list["Media"]] = relationship(
        cascade="all, delete",
        passive_deletes=True,

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

    async def delete(self):
        async with Session() as session:
            async with session.begin():
                await session.delete(self)

    @classmethod
    async def get_post(cls, post_number: int):
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
    async def get_post_by_id(cls, post_id: int):
        async with Session() as session:
            query = select(
                cls
            ).filter_by(
                id=post_id
            ).options(
                selectinload(cls.medias)
            ).options(
                selectinload(cls.user)
            )
            result = await session.execute(query)
            post: cls = result.scalars().one()
        return post

    @classmethod
    async def get_all_quantity(cls) -> int:
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

    async def update_in_db(self):
        async with Session() as session:
            async with session.begin():
                query = select(
                    type(self)
                ).filter_by(
                    id=self.id
                ).options(
                    selectinload(type(self).medias)
                )
                result = await session.execute(query)
                db_post: Post = result.scalars().one()

                if db_post.text != self.text:
                    db_post.text = self.text

                db_medias_id = [db_media.id for db_media in db_post.medias]
                new_medias_id = [new_media.id for new_media in self.medias]
                id_medias_to_delete = [db_media_id for db_media_id in db_medias_id if db_media_id not in new_medias_id]
        if id_medias_to_delete:
            await Media.delete(ids=id_medias_to_delete)

    @property
    def is_valid(self) -> bool:
        if self.is_empty:
            return False
        if self.medias:
            for media in self.medias:
                media.set_string_type()
            media_types_in_post = set([media.media_type for media in self.medias])
            if MediaTypes.document.value in media_types_in_post and len(media_types_in_post) > 1:
                return False
            if MediaTypes.audio.value in media_types_in_post and len(media_types_in_post) > 1:
                return False
        return True

    @property
    def is_empty(self) -> bool:
        if self.text or self.medias:
            return False
        return True


class Media(Base):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    file_id: Mapped[str]
    media_type: Mapped["MediaTypes"]

    @classmethod
    async def delete(cls, ids: list[int]):
        async with Session() as session:
            async with session.begin():
                query = delete(
                    cls
                ).filter(
                    cls.id.in_(ids)
                )
                await session.execute(query)

    def set_string_type(self):
        if isinstance(self.media_type, MediaTypes):
            self.media_type = self.media_type.value
