import enum

from aiogram.types import ContentType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from orm.base import Base


class MyEnum(enum.Enum):
    audio = "audio"
    video = "video"
    document = "document"
    photo = "photo"
    text = "text"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))

    caption: Mapped[str] = mapped_column(nullable=True)
    medias: Mapped[list["Media"]] = relationship()


class Media(Base):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    file_id: Mapped[str]
    media_type: Mapped[MyEnum]
