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
