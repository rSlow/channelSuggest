import asyncio

from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, ReplyKeyboardRemove

from bot import dp
from helpers.time_answer import TimeAnswer
from orm.users import User
from keyboads.start import StartKeyboard, BaseKeyboard


@dp.message_handler(Text(equals=BaseKeyboard.on_main_button), state="*")
async def on_main(message: Message):
    await start(message=message, answer="Возвращаю на главную...")



@dp.message_handler(state="*", commands=["start"])
async def start(message: Message, answer=None):
    user_id = message.from_user.id
    if user_id not in await User.get_all():
        await User.add(
            user_id=user_id,
            username=message.from_user.username
        )

    await message.answer(
        text=answer or TimeAnswer(message.date.time()),
        reply_markup=StartKeyboard()
    )
