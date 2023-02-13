import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from FSM.memory_storage import ModifiedMemoryStorage


class CustomBot(Bot):
    def __init__(self, *args, **kwargs):
        super(CustomBot, self).__init__(*args, **kwargs)
        self.admins = [int(user_id) for user_id in os.getenv("ADMIN_IDS").split(" ")]
        self.channel_id = os.getenv("CHANNEL_ID")


TOKEN = os.getenv("BOT_TOKEN")

storage = ModifiedMemoryStorage()
logging.basicConfig(level=logging.INFO)

bot = CustomBot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=storage)
