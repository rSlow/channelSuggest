from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from FSM.post_add import Start
from bot import dp, bot
from utils.time_answer import TimeAnswer
from ORM.users import User
from keyboads.start import StartKeyboard, BaseKeyboard


@dp.message_handler(Text(equals=BaseKeyboard.on_main_button), state="*")
async def on_main(message: Message):
    await start(message=message, answer="Возвращаю на главную...")


@dp.message_handler(state="*", commands=["start"])
async def start(message: Message, answer: str | None = None):
    user_id = message.from_user.id
    if answer is None and user_id not in await User.get_all():
        await User.add(
            user_id=user_id,
            fullname=message.from_user.full_name,
            mention=message.from_user.mention
        )

    await Start.start.set()

    is_user_admin = message.from_user.id in bot.admins
    await message.answer(
        text=answer or TimeAnswer(message.date.time()),
        reply_markup=StartKeyboard(
            add_admin_button=is_user_admin
        )
    )
