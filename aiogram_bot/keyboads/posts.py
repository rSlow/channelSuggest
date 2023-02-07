from aiogram.types import ReplyKeyboardMarkup

from ORM.posts import Post
from .base import BaseKeyboard


class AddPostKeyboard(BaseKeyboard):
    class Buttons:
        view = "Предпросмотр ➡"

    buttons_list = [
        Buttons.view,
    ]


class ConfirmPostKeyboard(BaseKeyboard):
    class Buttons:
        yes = "Да ✅"
        no = "Нет ❌"

    add_on_main_button = False

    buttons_list = [
        Buttons.yes,
        Buttons.no,
    ]


class UserPostKeyboard(ReplyKeyboardMarkup):
    class Buttons:
        next = ">"
        previous = "<"
        delete = "Удалить 🗑"

    def __init__(self, posts_quantity: int, current_post_number: int, *args, **kwargs):
        super().__init__(resize_keyboard=True, *args, **kwargs)

        if current_post_number > 1:
            self.add(self.Buttons.previous)
        self.insert(f"{current_post_number} / {posts_quantity}")
        if current_post_number < posts_quantity:
            self.insert(self.Buttons.next)

        self.row(self.Buttons.delete)
