from aiogram.types import Message


async def delete_center_button_message(message: Message):
    await message.delete()
