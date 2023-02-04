from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from orm.base import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))


class Media:
    pass
