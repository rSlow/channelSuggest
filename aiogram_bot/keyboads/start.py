import random

from aiogram.types import ReplyKeyboardRemove

from .base import BaseKeyboard


class StartKeyboard(BaseKeyboard):
    class Buttons:
        suggest = "Предложить пост"
        posts = "Мои посты"

    add_on_main_button = False
    buttons_list = [
        Buttons.suggest,
        Buttons.posts
    ]


class DiceKeyboard(BaseKeyboard):
    buttons_list = [
        "АСТАНАВИТЕСЬ"
    ]
    add_on_main_button = False
    input_field_placeholder = "А ну хватит играть!"

    @classmethod
    def get_random_keyboard(cls):
        if random.random() < 0.9:
            return ReplyKeyboardRemove()
        else:
            return cls()
