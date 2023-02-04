from asyncio import sleep

from aiogram.types import Message, ContentType
from aiogram.utils.exceptions import MessageCantBeDeleted

from bot import dp


@dp.message_handler(content_types=ContentType.ANY, state="*")
async def delete(message: Message):
    try:
        await message.delete()
    except MessageCantBeDeleted:
        pass

    msg = await message.answer("Читаем инструкцию и не спамим!")
    await sleep(2)
    await msg.delete()
