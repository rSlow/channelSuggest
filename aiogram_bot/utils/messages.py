import asyncio

from aiogram.types import Message


async def view_message_delete(message: Message):
    await message.delete()
    warning_message = await message.answer(
        text="Не надо так делать больше. Нажимаем только на кнопочки."
    )
    await asyncio.sleep(2)
    await warning_message.delete()
