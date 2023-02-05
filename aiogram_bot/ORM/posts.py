import enum

from aiogram.types import ContentType, MediaGroup
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

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

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))

    text: Mapped[str] = mapped_column(nullable=True)
    medias: Mapped[list["Media"]] = relationship()


class Media(Base):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    file_id: Mapped[str]
    media_type: Mapped["MediaTypes"]
