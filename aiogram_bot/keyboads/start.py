import random

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup

from .base import BaseKeyboard


class StartKeyboard(ReplyKeyboardMarkup):
    class Buttons:
        suggest = "Предложить пост"
        posts = "Мои посты"
        admin_posts = "Посты в очереди"

    def __init__(self, add_admin_button: bool = False):
        super().__init__(
            resize_keyboard=True,
            row_width=2,
        )
        self.add(self.Buttons.suggest)
        self.insert(self.Buttons.posts)
        if add_admin_button:
            self.add(self.Buttons.admin_posts)


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
