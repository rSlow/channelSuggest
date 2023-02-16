from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentTypes

from FSM.post_add import Start, AddPost
from ORM.posts import MediaTypesList
from bot import dp
from handlers.start import start
from keyboads.posts import AddPostKeyboard, ConfirmPostKeyboard, DeleteMediasKeyboard, EditTextKeyboard
from keyboads.start import StartKeyboard

from templates import render_template
from utils.exceptions import AudioMixedError, DocumentMixedError, TooMuchMediaError
from utils.messages import get_add_content_message, get_media_number
from utils.post_processors import parse_message, compile_post_message
from utils.proxy_interfaces.add import PostAddProxyInterface


@dp.message_handler(Text(equals=StartKeyboard.Buttons.suggest), state=Start.start)
async def suggest_post(message: Message, state: FSMContext):
    await AddPost.set_post.set()
    await PostAddProxyInterface.init(state=state)
    message_text = render_template(template_name="post_explain.jinja2")
    await message.answer(
        text=message_text,
        reply_markup=AddPostKeyboard()
    )


@dp.message_handler(Text(equals=EditTextKeyboard.Buttons.to_post), state=AddPost.edit_text)
@dp.message_handler(Text(equals=DeleteMediasKeyboard.Buttons.to_post), state=AddPost.del_medias)
@dp.message_handler(Text(equals=AddPostKeyboard.Buttons.view), state=AddPost.set_post)
async def preview_post(message: Message, state: FSMContext):
    post = await PostAddProxyInterface.get_post(state)

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
                reply_markup=ConfirmPostKeyboard(post=post)
            )

        else:
            try:
                post_message = compile_post_message(post=post)
                await message.answer_media_group(
                    media=post_message
                )
                await message.answer(
                    text="Отправляем пост?",
                    reply_markup=ConfirmPostKeyboard(post=post)
                )
            except (AudioMixedError, DocumentMixedError):
                await start(
                    message=message,
                    answer=f"Аудио или документы не может быть прикреплены совместно "
                           f"с другими видами медиафайлов. Пост отклонен."
                )


# it should be upper, but button of keyboard will be checked as text of media
@dp.message_handler(content_types=MediaTypesList, state=AddPost.set_post)
async def accept_media(message: Message, state: FSMContext):
    file_id, text, content_type = await parse_message(message=message)
    await message.delete()
    try:
        await PostAddProxyInterface.set_post_data(
            file_id=file_id,
            text=text,
            content_type=content_type,
            state=state
        )
        add_content_message_text = await get_add_content_message(state=state)
        await PostAddProxyInterface.send_explain_message(state=state, text=add_content_message_text)

    except TooMuchMediaError:
        PostAddProxyInterface.set_checking(user_id=state.user, flag=False)
        explain_message = PostAddProxyInterface.get_explain_message(user_id=state.user)
        if explain_message is not None:
            await explain_message.delete()

        await start(
            message=message,
            answer=f"Было прикреплено более 10 медиафайлов. Возможно прикрепление только до 10 файлов. Пост отклонен."
        )


@dp.message_handler(Text(equals=ConfirmPostKeyboard.Buttons.edit_text), state=AddPost.confirm_post)
async def edit_text(message: Message):
    await AddPost.edit_text.set()
    await message.answer(
        text=f"Ожидаю новый текст. Старый текст можно получить, нажав на кнопку "
             f"<pre>{EditTextKeyboard.Buttons.get_text}</pre>",
        reply_markup=EditTextKeyboard()
    )


@dp.message_handler(Text(equals=EditTextKeyboard.Buttons.get_text), state=AddPost.edit_text)
async def get_text(message: Message, state: FSMContext):
    post_text = await PostAddProxyInterface.get_text(state=state)
    await message.answer(text=post_text)


@dp.message_handler(content_types=ContentTypes.TEXT, state=AddPost.edit_text)
async def receive_new_text(message: Message, state: FSMContext):
    await PostAddProxyInterface.set_text(
        text=message.html_text,
        state=state
    )
    await preview_post(
        message=message,
        state=state
    )


@dp.message_handler(Text(equals=ConfirmPostKeyboard.Buttons.del_medias), state=AddPost.confirm_post)
async def delete_media_menu(message: Message, state: FSMContext, send_post_message: bool = False):
    await AddPost.del_medias.set()
    post = await PostAddProxyInterface.get_post(state=state)
    if send_post_message:
        await message.answer_media_group(
            media=compile_post_message(
                post=post,
                with_caption=False
            ),
        )
    await message.answer(
        text="Выберите фото для удаления:",
        reply_markup=DeleteMediasKeyboard(post=post)
    )


@dp.message_handler(regexp=r".+ [(]№\d+[)]", state=AddPost.del_medias)
async def delete_media(message: Message, state: FSMContext):
    media_number = get_media_number(text=message.text)
    await PostAddProxyInterface.delete_media(state=state, index=media_number - 1)
    updated_post = await PostAddProxyInterface.get_post(state=state)
    if updated_post.medias:
        await delete_media_menu(
            message=message,
            state=state,
            send_post_message=True
        )
    else:
        await preview_post(
            message=message,
            state=state
        )


@dp.message_handler(Text(equals=ConfirmPostKeyboard.Buttons.no), state=AddPost.confirm_post)
@dp.message_handler(Text(equals=ConfirmPostKeyboard.Buttons.yes), state=AddPost.confirm_post)
async def confirm_post(message: Message, state: FSMContext):
    if message.text == ConfirmPostKeyboard.Buttons.yes:
        post = await PostAddProxyInterface.get_post(state)
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
