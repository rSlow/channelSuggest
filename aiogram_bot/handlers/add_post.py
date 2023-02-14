from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from FSM.post_add import Start, AddPost
from ORM.posts import MediaTypesList
from bot import dp
from handlers.start import start
from keyboads.posts import AddPostKeyboard, ConfirmPostKeyboard
from keyboads.start import StartKeyboard
from templates.posts import POST_EXPLANATION_MESSAGE
from utils.exceptions import AudioMixedError, DocumentMixedError
from utils.post_processors import parse_message, set_data_in_post_proxy, compile_post_message
from utils.post_add_proxy import init_post_proxy, get_post_from_proxy


@dp.message_handler(Text(equals=StartKeyboard.Buttons.suggest), state=Start.start)
async def suggest_post(message: Message, state: FSMContext):
    await AddPost.set_post.set()
    await init_post_proxy(state=state)
    await message.answer(
        text=POST_EXPLANATION_MESSAGE,
        reply_markup=AddPostKeyboard()
    )


@dp.message_handler(Text(equals=AddPostKeyboard.Buttons.view), state=AddPost.set_post)
async def preview_post(message: Message, state: FSMContext):
    post = await get_post_from_proxy(state)

    if not post.text and not post.medias:
        await message.answer(
            text="Чтобы предложить пост, он должен иметь хотя бы один медиафайл или какой-либо текст."
        )
    else:
        await AddPost.confirm_post.set()

        if not post.medias:
            await message.answer(
                text=post.text
            )
            await message.answer(
                text="Отправляем пост?",
                reply_markup=ConfirmPostKeyboard()
            )

        else:
            try:
                post_message = await compile_post_message(post=post)
                await message.answer_media_group(
                    media=post_message
                )
                await message.answer(
                    text="Отправляем пост?",
                    reply_markup=ConfirmPostKeyboard()
                )
            except AudioMixedError:
                await start(
                    message=message,
                    answer="Аудио не может быть прикреплено совместно с другими видами медиафайлов. Пост отклонен."
                )
            except DocumentMixedError:
                await start(
                    message=message,
                    answer="Документ не может быть прикреплен совместно с другими видами медиафайлов. Пост отклонен."
                )


# "it should be upper, but button of keyboard will be checked as text of media"
@dp.message_handler(content_types=MediaTypesList, state=AddPost.set_post)
async def accept_media(message: Message, state: FSMContext):
    file_id, text, content_type = await parse_message(message=message)
    await set_data_in_post_proxy(
        file_id=file_id,
        text=text,
        content_type=content_type,
        state=state
    )
    await message.delete()


@dp.message_handler(Text(equals=ConfirmPostKeyboard.Buttons.no), state=AddPost.confirm_post)
@dp.message_handler(Text(equals=ConfirmPostKeyboard.Buttons.yes), state=AddPost.confirm_post)
async def confirm_post(message: Message, state: FSMContext):
    if message.text == ConfirmPostKeyboard.Buttons.yes:
        post = await get_post_from_proxy(state)
        await post.add()

        await start(
            message=message,
            answer="Пост предложен и скоро будет обработан."
        )
    else:
        await start(
            message=message,
            answer="Пост не сохранен. Возвращаемся в главное меню."
        )
