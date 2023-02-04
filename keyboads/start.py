from .base import BaseKeyboard


class StartKeyboard(BaseKeyboard):
    class Buttons:
        suggest = "Предложить пост"
        posts = "Мои посты"

    buttons_list = [
        Buttons.suggest,
        Buttons.posts
    ]
