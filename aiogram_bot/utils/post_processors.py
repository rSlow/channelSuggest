from aiogram.types import ContentType, Message, MediaGroup, ReplyKeyboardMarkup

from ORM.posts import Post, MediaTypes, Media
from keyboads.posts import DeleteMediasKeyboard
from utils.exceptions import MediaTypeError, DocumentMixedError, AudioMixedError


class PostMediaGroup(MediaGroup):
    def attach_media(self: MediaGroup, media: "Media", caption: str | None = None):
        if isinstance(media.media_type, MediaTypes):
            media.media_type = media.media_type.value

        match media.media_type:
            case MediaTypes.photo.value:
                self.attach_photo(
                    photo=media.file_id,
                    caption=caption
                )
            case MediaTypes.video.value:
                self.attach_video(
                    video=media.file_id,
                    caption=caption
                )
            case MediaTypes.audio.value:
                self.attach_audio(
                    audio=media.file_id,
                    caption=caption
                )
            case MediaTypes.document.value:
                self.attach_document(
                    document=media.file_id,
                    caption=caption
                )
            case _:
                raise MediaTypeError(media.media_type)


async def parse_message(message: Message):
    match message.content_type:
        case ContentType.PHOTO:
            file_id = message.photo[-1].file_id
        case ContentType.VIDEO:
            file_id = message.video.file_id
        case ContentType.AUDIO:
            file_id = message.audio.file_id
        case ContentType.DOCUMENT:
            file_id = message.document.file_id
        case ContentType.TEXT:
            file_id = None
        case _ as content_type:
            raise TypeError(f"unexpected content type format - {content_type}")

    try:
        text = message.html_text
    except TypeError:
        text = None
    content_type = message.content_type
    return file_id, text, content_type


def compile_post_message(post: Post, with_caption: bool = True):
    media_types_in_post = set([media.media_type for media in post.medias if media.media_type is not None])
    if MediaTypes.document.value in media_types_in_post and len(media_types_in_post) > 1:
        raise DocumentMixedError
    if MediaTypes.audio.value in media_types_in_post and len(media_types_in_post) > 1:
        raise AudioMixedError

    media_group = PostMediaGroup()

    for i, media in enumerate(post.medias, 0):
        if i == 0 and with_caption is True:
            caption = post.text
        else:
            caption = None

        media_group.attach_media(media=media, caption=caption)

    return media_group


async def send_post_message(message: Message,
                            post: Post,
                            second_info_message_text: str | None = None,
                            second_info_message_keyboard: ReplyKeyboardMarkup | None = None):
    if not post.medias:
        await message.answer(
            text=post.text
        )
    else:
        post_message = compile_post_message(
            post=post
        )
        await message.answer_media_group(
            media=post_message
        )

    if second_info_message_text is not None:
        await message.answer(
            text=second_info_message_text,
            reply_markup=second_info_message_keyboard
        )


async def send_delete_media_menu(message: Message, post: Post, resend_post: bool = False):
    if resend_post:
        await message.answer_media_group(
            media=compile_post_message(
                post=post,
                with_caption=False
            ),
        )
    await message.answer(
        text="Выберите медиафайл для удаления:",
        reply_markup=DeleteMediasKeyboard(post=post)
    )
