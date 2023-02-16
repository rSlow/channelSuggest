from aiogram.types import ReplyKeyboardMarkup

from ORM.posts import Post, MediaTypes
from utils.exceptions import MediaTypeError
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
        edit_text = "Редактировать текст ✏"
        del_medias = "Удаление медиафайлов 🗑"

    add_on_main_button = False

    buttons_list = [
        Buttons.yes,
        Buttons.no,
    ]

    def __init__(self, post: Post):
        super().__init__()
        if post.text is not None:
            self.add(self.Buttons.edit_text)

        if post.medias:
            self.insert(self.Buttons.del_medias)


class UserPostKeyboard(ReplyKeyboardMarkup):
    class Buttons:
        next = ">"
        previous = "<"
        delete = "Удалить 🗑"
        on_main = BaseKeyboard.on_main_button

    def __init__(self, posts_quantity: int, current_post_number: int, *args, **kwargs):
        super().__init__(resize_keyboard=True, *args, **kwargs)

        if current_post_number > 1:
            self.add(self.Buttons.previous)
        self.insert(f"{current_post_number} / {posts_quantity}")
        if current_post_number < posts_quantity:
            self.insert(self.Buttons.next)

        self.row(self.Buttons.delete)
        self.insert(self.Buttons.on_main)


class DeletePhotosKeyboard(ReplyKeyboardMarkup):
    def __init__(self, post: Post, *args, **kwargs):
        super().__init__(resize_keyboard=True, *args, **kwargs)

        for num, media in enumerate(post.medias, 1):
            match media.media_type:
                case MediaTypes.photo.value:
                    desc = "Фото"
                case MediaTypes.video.value:
                    desc = "Видео"
                case MediaTypes.audio.value:
                    desc = "Аудио"
                case MediaTypes.document.value:
                    desc = "Документ"
                case _:
                    raise MediaTypeError(media_type=media.media_type)

            self.insert(f"{desc} (№{num})")
