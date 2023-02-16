from collections.abc import Coroutine

from aiogram.dispatcher import FSMContext

from ORM.posts import Post
from utils.proxy_interfaces.base import ProxyInterface


class ViewProxyInterface(ProxyInterface):
    VIEW_POST = "view_post"
    POSTS_QUANTITY = "posts_quantity"
    CURRENT_VIEW_POST = "current_view_post"

    @classmethod
    async def init(cls,
                   state: FSMContext,
                   current_post: int,
                   update_posts_quantity: bool,
                   post_quantity_func: Coroutine):
        if await cls._get_data(state=state, key=cls.POSTS_QUANTITY,
                               default=False) is False or update_posts_quantity is True:
            posts_quantity = await post_quantity_func
            await cls._set_data(
                state=state,
                data={cls.POSTS_QUANTITY: posts_quantity}
            )
        await cls._set_data(
            state=state,
            data={cls.CURRENT_VIEW_POST: current_post}
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
            key=cls.CURRENT_VIEW_POST
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
