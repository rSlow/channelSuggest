import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode


class CustomBot(Bot):
    def __init__(self, *args, **kwargs):
        super(CustomBot, self).__init__(*args, **kwargs)
        self.admins = os.getenv("ADMIN_IDS").split(" ")
        self.channel_id = os.getenv("CHANNEL_ID")


TOKEN = os.getenv("BOT_TOKEN")

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

bot = CustomBot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=storage)
