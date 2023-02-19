from aiogram.types import ReplyKeyboardMarkup

from ORM.posts import Post, MediaTypes
from utils.exceptions import MediaTypeError
from .base import BaseKeyboard, PostsKeyboard


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


class UserPostKeyboard(PostsKeyboard):
    class Buttons(PostsKeyboard.Buttons):
        delete = "Удалить 🗑"
        on_main = BaseKeyboard.on_main_button

    buttons_lower_list = [
        Buttons.delete,
        Buttons.on_main
    ]


class DeleteMediasKeyboard(ReplyKeyboardMarkup):
    class Buttons:
        to_post = "Назад к посту 🔙"

    def __init__(self, post: Post, *args, **kwargs):
        super().__init__(resize_keyboard=True, *args, **kwargs)

        for num, media in enumerate(post.medias, 1):
            if isinstance(media.media_type, MediaTypes):
                media.media_type = media.media_type.value

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

        self.insert(self.Buttons.to_post)


class EditPostTextKeyboard(BaseKeyboard):
    class Buttons:
        get_text = "Получить текст 📜"
        del_text = "Удалить текст 🗑"
        to_post = "Назад к посту 🔙"

    buttons_list = [
        Buttons.get_text,
        Buttons.del_text,
        Buttons.to_post,
    ]
