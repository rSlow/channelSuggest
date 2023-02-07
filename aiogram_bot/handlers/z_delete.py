from asyncio import sleep

from aiogram.types import Message, ContentType
from aiogram.utils.exceptions import MessageCantBeDeleted

from bot import dp


@dp.message_handler(content_types=ContentType.ANY, state="*")
async def delete(message: Message, error_message: bool = True):
    try:
        await message.delete()
    except MessageCantBeDeleted:
        pass
    if error_message:
        msg = await message.answer("Не надо писать лишнее, я по пустякам не отвечаю.")
        await sleep(2)
        await msg.delete()
