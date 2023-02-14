from aiogram.dispatcher import FSMContext

from ORM.posts import Post

VIEW_POST = "view_post"
POSTS_QUANTITY = "posts_quantity"
CURRENT_VIEW_POST = "current_view_post"


async def init_posts_quantity_and_current(state: FSMContext,
                                          current_post: int,
                                          update_posts_quantity: bool):
    async with state.proxy() as data:
        if data.get(POSTS_QUANTITY, default=False) is False or update_posts_quantity is True:
            posts_quantity = await Post.get_user_posts_quantity(
                user_id=state.user
            )
            data[POSTS_QUANTITY] = posts_quantity
        data[CURRENT_VIEW_POST] = current_post


async def get_posts_quantity(state: FSMContext):
    async with state.proxy() as data:
        return data[POSTS_QUANTITY]


async def get_current_post_number(state: FSMContext):
    async with state.proxy() as data:
        return data[CURRENT_VIEW_POST]


async def set_post_in_proxy(state: FSMContext, post: Post):
    async with state.proxy() as data:
        data[VIEW_POST] = post


async def get_view_post_from_proxy(state: FSMContext):
    async with state.proxy() as data:
        return data[VIEW_POST]
