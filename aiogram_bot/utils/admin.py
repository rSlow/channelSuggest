import asyncio
from functools import wraps

from aiogram.types import Message


def admin_required(admins_list: list[int]):
    def wrapper(func):
        @wraps(func)
        async def inner(message: Message, *args, **kwargs):
            if message.from_user.id not in admins_list:
                await message.delete()
                warning_message = await message.answer(
                    text="Не лезь сюда, оно тебя сожрёт!"
                )
                await asyncio.sleep(2)
                await warning_message.delete()
            else:
                return await func(message, *args, **kwargs)

        return inner

    return wrapper
