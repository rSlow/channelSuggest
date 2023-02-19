from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentTypes

from FSM.post_admin_view import PostAdminView

from bot import dp
from handlers.post_admin_view import view_admin_suggest_post
from keyboads.admin import AdminPostsKeyboard, AdminEditPostTextKeyboard, AdminPostEditKeyboard
from keyboads.posts import DeleteMediasKeyboard
from templates import render_template
from utils.messages import get_media_number
from utils.post_processors import send_post_message, send_delete_media_menu
from utils.proxy_interfaces.admin import AdminProxyInterface


@dp.message_handler(Text(equals=AdminPostsKeyboard.Buttons.edit), state=PostAdminView.view)
async def edit_post(message: Message, state: FSMContext, view_post: bool = False):
    await PostAdminView.edit.set()
    current_post = await AdminProxyInterface.get_post(state=state)
    info_text = "Выберите действие:"
    keyboard = AdminPostEditKeyboard(post=current_post)
    if view_post:
        await send_post_message(
            message=message,
            post=current_post,
            second_info_message_text=info_text,
            second_info_message_keyboard=keyboard
        )
    else:
        await message.answer(
            text=info_text,
            reply_markup=AdminPostEditKeyboard(post=current_post)
        )


#######################

@dp.message_handler(Text(equals=AdminPostEditKeyboard.Buttons.edit_text), state=PostAdminView.edit)
async def edit_post_text(message: Message):
    await PostAdminView.edit_text.set()

    text_block = render_template(template_name="post_text_edit.jinja2")
    await message.answer(
        text=text_block,
        reply_markup=AdminEditPostTextKeyboard()
    )


@dp.message_handler(Text(equals=AdminEditPostTextKeyboard.Buttons.get_text), state=PostAdminView.edit_text)
async def get_post_text(message: Message, state: FSMContext):
    post_text = await AdminProxyInterface.get_post_text(state=state)
    await message.answer(post_text)


@dp.message_handler(Text(equals=AdminEditPostTextKeyboard.Buttons.decline), state=PostAdminView.edit_text)
async def decline_edit_post_text(message: Message, state: FSMContext):
    await message.answer(text="Отменяем изменение текста.")
    await edit_post(
        message=message,
        state=state,
        view_post=True
    )


@dp.message_handler(Text(equals=AdminEditPostTextKeyboard.Buttons.del_text), state=PostAdminView.edit_text)
async def delete_text(message: Message, state: FSMContext):
    updated_post = await AdminProxyInterface.get_post(state=state)
    if not updated_post.medias:
        await message.answer("Нельзя удалить текст, когда он является единственным содержимым поста.")
        await decline_edit_post_text(state=state, message=message)
    else:
        await AdminProxyInterface.remove_text(state=state)
        await edit_post(
            message=message,
            state=state,
            view_post=True
        )


@dp.message_handler(content_types=ContentTypes.TEXT, state=PostAdminView.edit_text)
async def accept_edit_post_text(message: Message, state: FSMContext):
    await AdminProxyInterface.set_post_text(state=state, text=message.html_text)

    await message.answer(text="Текст изменен.")
    await edit_post(
        message=message,
        state=state,
        view_post=True
    )


#######################

@dp.message_handler(Text(equals=AdminPostEditKeyboard.Buttons.del_medias), state=PostAdminView.edit)
async def delete_media_menu(message: Message, state: FSMContext, resend_post: bool = False):
    await PostAdminView.del_medias.set()
    post = await AdminProxyInterface.get_post(state=state)
    await send_delete_media_menu(
        message=message,
        post=post,
        resend_post=resend_post
    )


@dp.message_handler(regexp=r".+ [(]№\d+[)]", state=PostAdminView.del_medias)
async def delete_media(message: Message, state: FSMContext):
    media_number = get_media_number(text=message.text)
    await AdminProxyInterface.delete_media(state=state, index=media_number - 1)
    updated_post = await AdminProxyInterface.get_post(state=state)
    if updated_post.medias:
        await delete_media_menu(
            message=message,
            state=state,
            resend_post=True
        )
    elif updated_post.is_empty:
        await message.answer(
            text="В посте нужно оставить хотя бы один медиафайл или текст."
        )
        await cancel_post_changes(
            message=message,
            state=state
        )
    else:
        await edit_post(
            message=message,
            state=state,
            view_post=True
        )


@dp.message_handler(Text(equals=DeleteMediasKeyboard.Buttons.to_post), state=PostAdminView.del_medias)
async def back_to_post(message: Message, state: FSMContext):
    await edit_post(
        message=message,
        state=state,
        view_post=True
    )


#######################

@dp.message_handler(Text(equals=AdminPostEditKeyboard.Buttons.save), state=PostAdminView.edit)
async def save_post_changes(message: Message, state: FSMContext):
    current_post_number = await AdminProxyInterface.get_current_post_number(state=state)
    await AdminProxyInterface.save_post_to_db(state=state)
    await view_admin_suggest_post(
        message=message,
        state=state,
        post_number=current_post_number,
        update_posts_quantity=True
    )


@dp.message_handler(Text(equals=AdminPostEditKeyboard.Buttons.decline), state=PostAdminView.edit)
async def cancel_post_changes(message: Message, state: FSMContext):
    current_post_number = await AdminProxyInterface.get_current_post_number(state=state)
    await view_admin_suggest_post(
        message=message,
        state=state,
        post_number=current_post_number,
        update_posts_quantity=True
    )
