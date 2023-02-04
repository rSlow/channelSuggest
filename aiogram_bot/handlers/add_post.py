from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, ReplyKeyboardRemove

from FSM.post import Start, AddPost
from ORM.posts import MediaTypesList
from ORM.users import User
from bot import dp
from keyboads.start import StartKeyboard
from utils.proxy import init_post_proxy, add_text_to_post, add_media_to_post, get_post


@dp.message_handler(Text(equals=StartKeyboard.Buttons.suggest), state=Start.start)
async def suggest_post(message: Message, state: FSMContext):
    await AddPost.set_post.set()
    await init_post_proxy(state=state)
    await message.answer(
        text=f"Добавьте пост так, как вы хотите, чтобы он выглядел.\n"
             f"Можно добавить:\n"
             f" - фото\n"
             f" - видео\n"
             f" - описание к ним\n"
             f" - голый текст (без фото и т.д.)\n"
             f" - документ (в крайнем случае, добавление без причины - повод для отклонения поста)\n"
             f" - аудио (не голосовое - его бот попросту не примет)\n\n"
             f"После того как пост подготовлен - отправляйте, дальше будет предпросмотр "
             f"с утверждением поста или его отклонением.\n\n"
             f"<b>ОГРОМНАЯ ПРОСЬБА:</b> обращайте внимание на правила русского языка.",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(content_types=MediaTypesList, state=AddPost.set_post)
async def accept_media(message: Message, state: FSMContext):
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

    if text is not None:
        await add_text_to_post(text=text, state=state)
    if file_id is not None:
        await add_media_to_post(file_id=file_id, media_type=message.content_type, state=state)

    # post = await get_post(state)
    # await User.add_post(
    #     user_id=message.from_user.id,
    #     post=post
    # )
