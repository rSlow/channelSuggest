from aiogram.types import ReplyKeyboardMarkup

from ORM.posts import Post
from keyboads.base import BaseKeyboard, PostsKeyboard


class AdminEditPostTextKeyboard(BaseKeyboard):
    class Buttons:
        get_text = "Получить текст 📜"
        del_text = "Удалить текст 🗑"
        decline = "Отмена"

    add_on_main_button = False

    buttons_list = [
        Buttons.get_text,
        Buttons.del_text,
        Buttons.decline
    ]


class AdminPostsKeyboard(PostsKeyboard):
    class Buttons(PostsKeyboard.Buttons):
        edit = "Редактировать ✏"
        accept = "Опубликовать ✅"
        decline = "Отклонить ❌"
        on_main = BaseKeyboard.on_main_button

    buttons_lower_list = [
        Buttons.accept,
        Buttons.decline,
        Buttons.edit,
        Buttons.on_main,
    ]


class AdminPostEditKeyboard(ReplyKeyboardMarkup):
    class Buttons:
        edit_text = "Редактировать текст ✏"
        del_medias = "Удаление медиафайлов 🗑"
        save = "Сохранить изменения 💾"
        decline = "Отменить изменения 🙅"

    def __init__(self, post: Post, *args, **kwargs):
        super().__init__(resize_keyboard=True, row_width=2, *args, **kwargs)
        if post.text:
            self.insert(self.Buttons.edit_text)
        if post.medias:
            self.insert(self.Buttons.del_medias)

        self.insert(self.Buttons.save)
        self.insert(self.Buttons.decline)
