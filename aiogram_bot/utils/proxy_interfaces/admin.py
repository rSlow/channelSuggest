from aiogram.dispatcher import FSMContext

from ORM.posts import Post
from utils.proxy_interfaces.view import ViewProxyInterface


class AdminProxyInterface(ViewProxyInterface):
    VIEW_POST = "view_admin_post"
    POSTS_QUANTITY = "admin_posts_quantity"
    CURRENT_VIEW_POST = "admin_current_view_post"

    @classmethod
    async def get_post_text(cls, state: FSMContext) -> str:
        post: Post = await cls._get_data(
            state=state,
            key=cls.VIEW_POST
        )
        return post.text
