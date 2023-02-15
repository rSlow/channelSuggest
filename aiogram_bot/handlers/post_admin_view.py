from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentTypes

from FSM.post_add import Start
from FSM.post_admin_view import PostAdminView
from ORM.posts import Post

from bot import dp, bot
from handlers.start import start
from handlers.unregistered import delete_center_button_message
from keyboads.admin import AdminPostKeyboard, AdminEditPostTextKeyboard
from keyboads.start import StartKeyboard
from templates import render_template
from utils.admin import admin_required
from utils.messages import view_message_delete
from utils.post_processors import compile_post_message
from utils.proxy_interface import ProxyAdminInterface


@dp.message_handler(Text(equals=StartKeyboard.Buttons.admin_posts), state=Start.start)
@admin_required(admins_list=bot.admins)
async def view_admin_suggest_post(message: Message,
                                  state: FSMContext,
                                  post_number: int = 1,
                                  current: bool = False,
                                  update_posts_quantity: bool = True):
    if not current:
        await ProxyAdminInterface.init(
            state=state,
            current_post=post_number,
            update_posts_quantity=update_posts_quantity,
            post_quantity_func=Post.get_all_quantity()
        )
    posts_quantity = await ProxyAdminInterface.get_posts_quantity(
        state=state
    )

    if posts_quantity == 0:
        await start(
            message=message,
            answer="Постов нет в очереди."
        )
    else:
        await PostAdminView.view.set()
        post = await Post.get_all(
            post_number=post_number
        )
        await ProxyAdminInterface.set_post(
            state=state,
            post=post
        )

        if not post.medias:
            await message.answer(
                text=post.text
            )
        else:
            post_message = await compile_post_message(
                post=post
            )
            await message.answer_media_group(
                media=post_message
            )

        user_block = render_template(
            template_name="user_block.jinja2",
            data={
                "user_mention": post.user.mention,
                "user_id": post.user.id,
                "user_fullname": post.user.fullname,
            }
        )
        await message.answer(
            text=user_block,
            reply_markup=AdminPostKeyboard(
                posts_quantity=posts_quantity,
                current_post_number=post_number
            )
        )


dp.register_message_handler(callback=delete_center_button_message, regexp=r"\d+\s[/]\s\d", state=PostAdminView.view)


@dp.message_handler(Text(equals=AdminPostKeyboard.Buttons.previous), state=PostAdminView.view)
async def get_previous_post(message: Message, state: FSMContext):
    previous_post_number = await ProxyAdminInterface.get_current_post_number(state=state) - 1

    if previous_post_number == 0:
        await view_message_delete(message)
    else:
        await view_admin_suggest_post(
            message=message,
            state=state,
            post_number=previous_post_number,
            update_posts_quantity=False
        )


@dp.message_handler(Text(equals=AdminPostKeyboard.Buttons.next), state=PostAdminView.view)
async def get_next_post(message: Message, state: FSMContext):
    next_post_number = await ProxyAdminInterface.get_current_post_number(state=state) + 1
    posts_quantity = await ProxyAdminInterface.get_posts_quantity(state=state)

    if next_post_number > posts_quantity:
        await view_message_delete(message)
    else:
        await view_admin_suggest_post(
            message=message,
            state=state,
            post_number=next_post_number,
            update_posts_quantity=False
        )


@dp.message_handler(Text(equals=AdminPostKeyboard.Buttons.edit), state=PostAdminView.view)
async def start_edit_post_text(message: Message, state: FSMContext):
    await PostAdminView.edit_text.set()

    text_block = render_template(template_name="post_text_edit.jinja2")
    await message.answer(
        text=text_block,
        reply_markup=AdminEditPostTextKeyboard()
    )


@dp.message_handler(Text(equals=AdminEditPostTextKeyboard.Buttons.get_text), state=PostAdminView.edit_text)
async def get_post_text(message: Message, state: FSMContext):
    post_text = await ProxyAdminInterface.get_post_text(state=state)
    await message.answer(
        text=f"<code>{post_text}</code>"
    )


@dp.message_handler(Text(equals=AdminEditPostTextKeyboard.Buttons.decline), state=PostAdminView.edit_text)
async def decline_edit_post_text(message: Message, state: FSMContext):
    await message.answer(text="Отменяем изменение текста.")
    await view_admin_suggest_post(
        message=message,
        state=state,
        current=True
    )


@dp.message_handler(content_types=ContentTypes.TEXT, state=PostAdminView.edit_text)
async def accept_edit_post_text(message: Message, state: FSMContext):
    current_post_number = await ProxyAdminInterface.get_current_post_number(state=state)
    post = await ProxyAdminInterface.get_post(state=state)
    await post.set_text(text=message.html_text)

    await message.answer(text="Текст изменен.")
    await view_admin_suggest_post(
        message=message,
        state=state,
        post_number=current_post_number,
        update_posts_quantity=False
    )


@dp.message_handler(Text(equals=AdminPostKeyboard.Buttons.accept), state=PostAdminView.view)
async def accept_post(message: Message, state: FSMContext):
    pass


@dp.message_handler(Text(equals=AdminPostKeyboard.Buttons.decline), state=PostAdminView.view)
async def decline_post(message: Message, state: FSMContext):
    pass
