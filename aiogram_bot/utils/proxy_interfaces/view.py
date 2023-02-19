from collections.abc import Coroutine

from aiogram.dispatcher import FSMContext

from ORM.posts import Post
from utils.proxy_interfaces.base import ProxyInterface


class ViewProxyInterface(ProxyInterface):
    VIEW_POST = "view_post"
    POSTS_QUANTITY = "posts_quantity"
    CURRENT_VIEW_POST_NUMBER = "current_view_post_number"

    @classmethod
    async def init(cls,
                   state: FSMContext,
                   current_post_number: int | None,
                   update_posts_quantity: bool,
                   posts_quantity_coroutine: Coroutine):
        if update_posts_quantity is True or await cls.get_posts_quantity(state=state) is None:
            posts_quantity = await posts_quantity_coroutine
            await cls._set_data(
                state=state,
                data={cls.POSTS_QUANTITY: posts_quantity}
            )
        else:
            posts_quantity_coroutine.close()

        if current_post_number is None or current_post_number == 0:
            current_post_number = 1
        await cls._set_data(
            state=state,
            data={cls.CURRENT_VIEW_POST_NUMBER: current_post_number}
        )

    @classmethod
    async def get_posts_quantity(cls, state: FSMContext) -> int:
        return await cls._get_data(
            state=state,
            key=cls.POSTS_QUANTITY
        )

    @classmethod
    async def get_current_post_number(cls, state: FSMContext) -> int:
        return await cls._get_data(
            state=state,
            key=cls.CURRENT_VIEW_POST_NUMBER
        )

    @classmethod
    async def set_post(cls, state: FSMContext, post: Post):
        await cls._set_data(
            state=state,
            data={cls.VIEW_POST: post}
        )

    @classmethod
    async def get_post(cls, state: FSMContext) -> Post:
        return await cls._get_data(
            state=state,
            key=cls.VIEW_POST
        )

    @classmethod
    async def set_post_text(cls, text: str, state: FSMContext):
        async with state.proxy() as data:
            post: Post = data[cls.VIEW_POST]
            post.text = text
