from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentTypes

from FSM.post_add import Start, AddPost
from ORM.posts import MediaTypesList
from bot import dp
from handlers.start import start
from keyboads.posts import AddPostKeyboard, ConfirmPostKeyboard, DeleteMediasKeyboard, EditPostTextKeyboard
from keyboads.start import StartKeyboard

from templates import render_template
from utils.exceptions import TooMuchMediaError
from utils.messages import get_add_content_message, get_media_number
from utils.post_processors import parse_message, send_delete_media_menu, send_post_message
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


@dp.message_handler(Text(equals=EditPostTextKeyboard.Buttons.to_post), state=AddPost.edit_text)
@dp.message_handler(Text(equals=DeleteMediasKeyboard.Buttons.to_post), state=AddPost.del_medias)
@dp.message_handler(Text(equals=AddPostKeyboard.Buttons.view), state=AddPost.set_post)
async def preview_post(message: Message, state: FSMContext):
    post = await PostAddProxyInterface.get_post(state)

    if post.is_empty:
        await start(
            message=message,
            answer=f"Пустой пост нельзя выложить. Нужно отправить хотя бы один медиафайл или текст. "
                   f"Возвращаю в главное меню."
        )
    elif post.is_valid:
        await AddPost.confirm_post.set()
        await send_post_message(
            message=message,
            post=post,
            second_info_message_keyboard=ConfirmPostKeyboard(post=post),
            second_info_message_text="Отправляем пост?"
        )
    else:
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
        await PostAddProxyInterface.cancel_check(user_id=state.user)
        await start(
            message=message,
            answer=f"Было прикреплено более 10 медиафайлов. Возможно прикрепление только до 10 файлов. Пост отклонен."
        )


@dp.message_handler(Text(equals=ConfirmPostKeyboard.Buttons.edit_text), state=AddPost.confirm_post)
async def edit_text(message: Message):
    await AddPost.edit_text.set()
    await message.answer(
        text=f"Ожидаю новый текст. Старый текст можно получить, нажав на кнопку "
             f"<pre>{EditPostTextKeyboard.Buttons.get_text}</pre>",
        reply_markup=EditPostTextKeyboard()
    )


@dp.message_handler(Text(equals=EditPostTextKeyboard.Buttons.get_text), state=AddPost.edit_text)
async def get_text(message: Message, state: FSMContext):
    post_text = await PostAddProxyInterface.get_text(state=state)
    await message.answer(text=post_text)


@dp.message_handler(Text(equals=EditPostTextKeyboard.Buttons.del_text), state=AddPost.edit_text)
async def delete_text(message: Message, state: FSMContext):
    await PostAddProxyInterface.remove_text(state=state)
    await preview_post(
        message=message,
        state=state
    )


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
async def delete_media_menu(message: Message, state: FSMContext, resend_post: bool = False):
    await AddPost.del_medias.set()
    post = await PostAddProxyInterface.get_post(state=state)
    await send_delete_media_menu(
        message=message,
        post=post,
        resend_post=resend_post
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
            resend_post=True
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
