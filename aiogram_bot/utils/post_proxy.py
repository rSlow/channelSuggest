from aiogram.dispatcher import FSMContext

from ORM.posts import Post, MediaTypesList, Media

POST = "post"


async def init_post_proxy(state: FSMContext):
    async with state.proxy() as data:
        data[POST] = Post()


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
