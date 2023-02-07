from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message, MediaGroup

from ORM.posts import Post, MediaTypes, Media
from utils.post_proxy import add_text_to_post, add_media_to_post


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
                raise TypeError(f"unexpected media type - {media.media_type}")


class AudioMixedError(TypeError):
    pass


class DocumentMixedError(TypeError):
    pass


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


async def set_data_in_post_proxy(
        file_id: str | None,
        text: str | None,
        content_type: str,
        state: FSMContext
):
    if text is not None:
        await add_text_to_post(text=text, state=state)
    if file_id is not None:
        await add_media_to_post(file_id=file_id, media_type=content_type, state=state)


async def compile_post_message(post: Post):
    media_types_in_post = set([media.media_type for media in post.medias if media.media_type is not None])
    if MediaTypes.document.value in media_types_in_post and len(media_types_in_post) > 1:
        raise DocumentMixedError
    if MediaTypes.audio.value in media_types_in_post and len(media_types_in_post) > 1:
        raise AudioMixedError

    media_group = PostMediaGroup()
    first_media: "Media" = post.medias[0]
    media_group.attach_media(
        media=first_media,
        caption=post.text
    )

    for media in post.medias[1:]:
        media_group.attach_media(media=media)

    return media_group


