from typing import Any

from aiogram.dispatcher import FSMContext

from ORM.posts import Post


class ProxyInterface:
    VIEW_POST = "view_post"
    POSTS_QUANTITY = "posts_quantity"
    CURRENT_VIEW_POST = "current_view_post"

    @staticmethod
    async def get_data(state: FSMContext, key: str, default: Any = None):
        data = await state.get_data()
        try:
            value: Any = data[key]
        except KeyError:
            if default is not None:
                value = default
            else:
                raise
        return value

    @staticmethod
    async def set_data(state: FSMContext, data: dict):
        new_data = await state.get_data()
        new_data.update(data)
        await state.set_data(data=new_data)

    @classmethod
    async def init(cls,
                   state: FSMContext,
                   current_post: int,
                   update_posts_quantity: bool):

        if cls.get_data(state=state, key=cls.POSTS_QUANTITY, default=False) is False or update_posts_quantity is True:
            posts_quantity = await Post.get_user_posts_quantity(
                user_id=state.user
            )
            await cls.set_data(
                state=state,
                data={cls.POSTS_QUANTITY: posts_quantity}
            )
        await cls.set_data(
            state=state,
            data={cls.CURRENT_VIEW_POST: current_post}
        )

    @classmethod
    async def get_posts_quantity(cls, state: FSMContext):
        return await cls.get_data(
            state=state,
            key=cls.POSTS_QUANTITY
        )

    @classmethod
    async def get_current_post_number(cls, state: FSMContext):
        return await cls.get_data(
            state=state,
            key=cls.CURRENT_VIEW_POST
        )

    @classmethod
    async def set_post(cls, state: FSMContext, post: Post):
        await cls.set_data(
            state=state,
            data={cls.VIEW_POST: post}
        )

    @classmethod
    async def get_post(cls, state: FSMContext):
        return await cls.get_data(
            state=state,
            key=cls.VIEW_POST
        )


class ProxyAdminInterface(ProxyInterface):
    VIEW_POST = "view_admin_post"
    POSTS_QUANTITY = "admin_posts_quantity"
    CURRENT_VIEW_POST = "admin_current_view_post"
