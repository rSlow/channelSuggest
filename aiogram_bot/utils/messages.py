import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from ORM.posts import media_annotations
from templates import render_template
from utils.proxy_interfaces.add import PostAddProxyInterface


async def view_message_delete(message: Message):
    await message.delete()
    warning_message = await message.answer(
        text="Не надо так делать больше. Нажимаем только на кнопочки."
    )
    await asyncio.sleep(2)
    await warning_message.delete()


async def get_add_content_message(state: FSMContext):
    post = await PostAddProxyInterface.get_post(state=state)

    return render_template(
        template_name="post_receive.jinja2",
        data={
            "post": post,
            "media_annotations": media_annotations
        }
    )


def get_media_number(text: str):
    _, second_block = text.split()
    return int(second_block[2:-1])
