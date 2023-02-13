from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from FSM.post_add import Start

from bot import dp, bot
from keyboads.start import StartKeyboard
from utils.admin import admin_required


@dp.message_handler(Text(equals=StartKeyboard.Buttons.admin_posts), state=Start.start)
@admin_required(admins_list=bot.admins)
async def view_admin_suggest_post(message: Message, state: FSMContext):
    pass
