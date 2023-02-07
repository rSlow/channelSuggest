from aiogram.dispatcher import FSMContext

from ORM.posts import Post, MediaTypesList, Media
from ORM.users import User

POST = "post"
VIEW_POST = "view_post"
POSTS_QUANTITY = "posts_quantity"
CURRENT_VIEW_POST = "current_view_post"


async def init_post_proxy(state: FSMContext, user_id: int):
    async with state.proxy() as data:
        data[POST] = Post(
            user_id=user_id
        )


async def add_text_to_post(text: str, state: FSMContext):
    async with state.proxy() as data:
        post: Post = data[POST]
        if post.text is None:
            post.text = text


async def add_media_to_post(file_id: str, media_type: str, state: FSMContext):
    if media_type not in MediaTypesList:
        raise TypeError(f"{media_type} not expected as media type")
    else:
        async with state.proxy() as data:
            post: Post = data[POST]
            post.medias.append(
                Media(file_id=file_id, media_type=media_type)
            )


async def get_post_from_proxy(state: FSMContext):
    async with state.proxy() as data:
        return data[POST]


async def init_posts_quantity_and_current(state: FSMContext,
                                          user_id: int,
                                          current_post: int,
                                          update_posts_quantity: bool):
    async with state.proxy() as data:
        if data.get(POSTS_QUANTITY, default=False) is False or update_posts_quantity is True:
            posts_quantity = await Post.get_user_posts_quantity(
                user_id=user_id
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
