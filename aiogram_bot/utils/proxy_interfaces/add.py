import asyncio
from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.exceptions import MessageToDeleteNotFound

from ORM.posts import Post, MediaTypesList, Media
from bot import bot
from utils.exceptions import MediaTypeError, TooMuchMediaError
from utils.proxy_interfaces.base import ProxyInterface


class PostAddProxyInterface(ProxyInterface):
    POST = "post"

    EXPLAIN_MESSAGE_TEXT: str | None = None
    EXPLAIN_MESSAGE = None
    ALLOWED_SEND_EXPLAIN_MESSAGE = False
    CHECKING = False

    @classmethod
    async def init(cls, state: FSMContext):
        await cls._set_data(
            state=state,
            data={
                cls.POST: Post(user_id=state.user),
                cls.EXPLAIN_MESSAGE_TEXT: None
            }
        )

    @classmethod
    async def add_text(cls, text: str, state: FSMContext):
        async with state.proxy() as data:
            post: Post = data[cls.POST]
            if post.text is None:
                post.text = text

    @classmethod
    async def add_media(cls, file_id: str, media_type: str, state: FSMContext):
        if media_type not in MediaTypesList:
            raise MediaTypeError(media_type)
        else:
            async with state.proxy() as data:
                post: Post = data[cls.POST]
                if len(post.medias) > 10:
                    raise TooMuchMediaError
                else:
                    post.medias.append(
                        Media(file_id=file_id, media_type=media_type)
                    )

    @classmethod
    async def set_post_data(cls,
                            file_id: str | None,
                            text: str | None,
                            content_type: str,
                            state: FSMContext):
        if text is not None:
            await cls.add_text(text=text, state=state)
        if file_id is not None:
            await cls.add_media(file_id=file_id, media_type=content_type, state=state)

    @classmethod
    async def get_post(cls, state: FSMContext) -> Post:
        return await cls._get_data(state=state, key=cls.POST)

    @classmethod
    async def send_explain_message(cls, state: FSMContext, text: str):
        cls.CHECKING = True
        while cls.CHECKING:
            if cls.ALLOWED_SEND_EXPLAIN_MESSAGE:
                cls.CHECKING = False

                explain_message_text = cls.EXPLAIN_MESSAGE_TEXT
                explain_message = await bot.send_message(
                    chat_id=state.chat,
                    text=explain_message_text
                )
                if cls.EXPLAIN_MESSAGE is not None:
                    await cls.EXPLAIN_MESSAGE.delete()
                cls.EXPLAIN_MESSAGE = explain_message

                cls.ALLOWED_SEND_EXPLAIN_MESSAGE = False

                break

            else:
                cls.EXPLAIN_MESSAGE_TEXT = text
                await asyncio.sleep(1)
                if cls.CHECKING:
                    cls.ALLOWED_SEND_EXPLAIN_MESSAGE = True
