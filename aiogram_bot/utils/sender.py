import os

from ORM.posts import Post
from bot import bot
from utils.post_processors import compile_post_message


async def send_post(post: Post):
    if not post.medias:
        await bot.send_message(
            chat_id=os.getenv("CHANNEL_ID"),
            text=post.text
        )
    else:
        post_media_group = compile_post_message(post=post)
        await bot.send_media_group(
            chat_id=os.getenv("CHANNEL_ID"),
            media=post_media_group
        )
