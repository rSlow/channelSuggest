import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from ORM.posts import Post, MediaTypesList, Media
from bot import bot
from utils.exceptions import MediaTypeError, TooMuchMediaError
from utils.proxy_interfaces.base import ProxyInterface


class PostAddProxyInterface(ProxyInterface):
    POST = "post"

    POST_ADD_KW = {}
    EXPLAIN_MESSAGE_TEXT = "explain_message_text"
    EXPLAIN_MESSAGE = "explain_message"
    ALLOW_SEND_EXPLAIN_MESSAGE = "allow_send_explain_message"
    CHECKING = "checking"

    @classmethod
    def get_checking(cls, user_id: int) -> bool:
        return cls.POST_ADD_KW[user_id][cls.CHECKING]

    @classmethod
    def set_checking(cls, user_id: int, flag: bool):
        cls.POST_ADD_KW[user_id][cls.CHECKING] = flag

    @classmethod
    def get_explain_message(cls, user_id: int) -> Message:
        return cls.POST_ADD_KW[user_id][cls.EXPLAIN_MESSAGE]

    @classmethod
    async def init(cls, state: FSMContext):
        await cls._set_data(
            state=state,
            data={
                cls.POST: Post(user_id=state.user),
            }
        )
        cls.POST_ADD_KW[state.user] = {
            cls.EXPLAIN_MESSAGE_TEXT: None,
            cls.EXPLAIN_MESSAGE: None,
            cls.ALLOW_SEND_EXPLAIN_MESSAGE: False,
            cls.CHECKING: False
        }

    @classmethod
    async def set_text(cls, text: str, state: FSMContext):
        async with state.proxy() as data:
            post: Post = data[cls.POST]
            post.text = text

    @classmethod
    async def remove_text(cls, state: FSMContext):
        async with state.proxy() as data:
            post: Post = data[cls.POST]
            post.text = None

    @classmethod
    async def get_text(cls, state: FSMContext) -> str:
        async with state.proxy() as data:
            post: Post = data[cls.POST]
            return post.text

    @classmethod
    async def add_media(cls, file_id: str, media_type: str, state: FSMContext):
        if media_type not in MediaTypesList:
            raise MediaTypeError(media_type)
        else:
            async with state.proxy() as data:
                post: Post = data[cls.POST]
                post.medias.append(
                    Media(file_id=file_id, media_type=media_type)
                )
                if len(post.medias) > 10:
                    raise TooMuchMediaError

    @classmethod
    async def set_post_data(cls,
                            file_id: str | None,
                            text: str | None,
                            content_type: str,
                            state: FSMContext):
        if text is not None:
            await cls.set_text(text=text, state=state)
        if file_id is not None:
            await cls.add_media(file_id=file_id, media_type=content_type, state=state)

    @classmethod
    async def get_post(cls, state: FSMContext) -> Post:
        return await cls._get_data(state=state, key=cls.POST)

    @classmethod
    async def delete_media(cls, state: FSMContext, index: int):
        async with state.proxy() as data:
            post = data[cls.POST]
            medias_list: list = post.medias[:]
            medias_list.pop(index)
            post.medias = medias_list

    ##################

    @classmethod
    async def send_explain_message(cls, state: FSMContext, text: str):
        user_data = cls.POST_ADD_KW[state.user]
        user_data[cls.CHECKING] = True

        while user_data[cls.CHECKING]:
            if user_data[cls.ALLOW_SEND_EXPLAIN_MESSAGE]:

                user_data[cls.CHECKING] = False
                user_data[cls.ALLOW_SEND_EXPLAIN_MESSAGE] = False

                if user_data[cls.EXPLAIN_MESSAGE] is not None:
                    await user_data[cls.EXPLAIN_MESSAGE].delete()

                user_data[cls.EXPLAIN_MESSAGE] = await bot.send_message(
                    chat_id=state.chat,
                    text=user_data[cls.EXPLAIN_MESSAGE_TEXT]
                )

                break

            else:
                user_data[cls.EXPLAIN_MESSAGE_TEXT] = text
                await asyncio.sleep(1)
                if user_data[cls.CHECKING]:
                    user_data[cls.ALLOW_SEND_EXPLAIN_MESSAGE] = True

    @classmethod
    async def cancel_check(cls, user_id: int):
        cls.set_checking(user_id=user_id, flag=False)
        explain_message = cls.get_explain_message(user_id=user_id)
        if explain_message is not None:
            await explain_message.delete()
