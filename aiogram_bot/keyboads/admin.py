from aiogram.types import ReplyKeyboardMarkup

from keyboads.base import BaseKeyboard


class AdminEditPostTextKeyboard(BaseKeyboard):
    class Buttons:
        get_text = "Сообщение с текстом"
        decline = "Отмена"

    add_on_main_button = False

    buttons_list = [
        Buttons.get_text,
        Buttons.decline
    ]


class AdminPostKeyboard(ReplyKeyboardMarkup):
    class Buttons:
        next = ">"
        previous = "<"
        edit = "Редактировать ✏"
        accept = "Опубликовать ✅"
        decline = "Отклонить ❌"
        on_main = BaseKeyboard.on_main_button

    def __init__(self, posts_quantity: int, current_post_number: int, *args, **kwargs):
        super().__init__(resize_keyboard=True, *args, **kwargs)

        if current_post_number > 1:
            self.add(self.Buttons.previous)
        self.insert(f"{current_post_number} / {posts_quantity}")
        if current_post_number < posts_quantity:
            self.insert(self.Buttons.next)

        self.row(self.Buttons.accept)
        self.insert(self.Buttons.decline)

        self.row(self.Buttons.edit)
        self.insert(self.Buttons.on_main)
