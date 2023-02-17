from aiogram.dispatcher import FSMContext

from ORM.posts import Post
from utils.proxy_interfaces.view import ViewProxyInterface


class AdminProxyInterface(ViewProxyInterface):
    VIEW_POST = "view_admin_post"
    POSTS_QUANTITY = "admin_posts_quantity"
    CURRENT_VIEW_POST_NUMBER = "admin_current_view_post_number"

    @classmethod
    async def get_post_text(cls, state: FSMContext) -> str:
        post: Post = await cls._get_data(
            state=state,
            key=cls.VIEW_POST
        )
        return post.text

    @classmethod
    async def save_post_to_db(cls, state: FSMContext):
        post: Post = await cls._get_data(
            state=state,
            key=cls.VIEW_POST
        )
        await post.update_in_db()

    @classmethod
    async def delete_media(cls, state: FSMContext, index: int):
        async with state.proxy() as data:
            post = data[cls.VIEW_POST]
            medias_list: list = post.medias[:]
            medias_list.pop(index)
            post.medias = medias_list
