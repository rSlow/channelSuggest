from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from FSM.post_add import Start
from FSM.post_admin_view import PostAdminView
from ORM.posts import Post

from bot import dp, bot
from handlers.start import start
from handlers.unregistered import delete_center_button_message
from keyboads.posts import AdminPostKeyboard
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
                                  update_posts_quantity: bool = True):
    await ProxyAdminInterface.init(
        state=state,
        current_post=post_number,
        update_posts_quantity=update_posts_quantity,
        post_quantity_func=Post.get_posts_quantity()
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
        post = await Post.get_post(
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
            "user_mention": message.from_user.mention,
            "user_id": message.from_user.id,
            "user_fullname": message.from_user.full_name,
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
