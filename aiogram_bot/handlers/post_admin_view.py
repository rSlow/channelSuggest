from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from FSM.post_add import Start
from FSM.post_admin_view import PostAdminView
from ORM.posts import Post

from bot import dp
from handlers.start import start
from handlers.unregistered import delete_center_button_message
from keyboads.admin import AdminPostKeyboard
from keyboads.start import StartKeyboard
from templates import render_template
from utils.admin import admin_required
from utils.messages import view_message_delete
from utils.post_processors import send_post_message
from utils.proxy_interfaces.admin import AdminProxyInterface
from utils.sender import send_post_to_channel


@dp.message_handler(Text(equals=StartKeyboard.Buttons.admin_posts), state=Start.start)
@admin_required(admins_list=dp.bot.admins)
async def view_admin_suggest_post(message: Message,
                                  state: FSMContext,
                                  post_number: int | None = None,
                                  current: bool = False,
                                  update_posts_quantity: bool = True):
    if not current:
        try:
            if post_number is None:
                post_number = 1
            await AdminProxyInterface.init(
                state=state,
                current_post_number=post_number,
                update_posts_quantity=update_posts_quantity,
                post_quantity_func=Post.get_all_quantity()
            )
        except RuntimeWarning:
            pass

    posts_quantity = await AdminProxyInterface.get_posts_quantity(
        state=state
    )

    if posts_quantity == 0:
        await start(
            message=message,
            answer="Постов нет в очереди."
        )
    else:
        await PostAdminView.view.set()
        current_post_number = await AdminProxyInterface.get_current_post_number(state=state)
        post = await Post.get_post(
            post_number=current_post_number
        )
        await AdminProxyInterface.set_post(
            state=state,
            post=post
        )

        user_text_block = render_template(
            template_name="user_block.jinja2",
            data={
                "user_mention": post.user.mention,
                "user_id": post.user.id,
                "user_fullname": post.user.fullname,
            }
        )

        await send_post_message(
            message=message,
            post=post,
            second_info_message_text=user_text_block,
            second_info_message_keyboard=AdminPostKeyboard(
                posts_quantity=posts_quantity,
                current_post_number=current_post_number
            )
        )


dp.register_message_handler(callback=delete_center_button_message, regexp=r"\d+\s[/]\s\d", state=PostAdminView.view)


@dp.message_handler(Text(equals=AdminPostKeyboard.Buttons.previous), state=PostAdminView.view)
async def get_previous_post(message: Message, state: FSMContext):
    previous_post_number = await AdminProxyInterface.get_current_post_number(state=state) - 1

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
    next_post_number = await AdminProxyInterface.get_current_post_number(state=state) + 1
    posts_quantity = await AdminProxyInterface.get_posts_quantity(state=state)

    if next_post_number > posts_quantity:
        await view_message_delete(message)
    else:
        await view_admin_suggest_post(
            message=message,
            state=state,
            post_number=next_post_number,
            update_posts_quantity=False
        )


@dp.message_handler(Text(equals=AdminPostKeyboard.Buttons.accept), state=PostAdminView.view)
async def accept_post(message: Message, state: FSMContext):
    post = await AdminProxyInterface.get_post(state=state)
    await send_post_to_channel(post=post)
    await post.delete()

    await message.answer("Пост опубликован.")

    current_post_number = await AdminProxyInterface.get_current_post_number(state=state)
    posts_quantity = await AdminProxyInterface.get_posts_quantity(state=state)
    if current_post_number == posts_quantity:
        current_post_number -= 1

    await view_admin_suggest_post(
        message=message,
        state=state,
        post_number=current_post_number,
        update_posts_quantity=True
    )


@dp.message_handler(Text(equals=AdminPostKeyboard.Buttons.decline), state=PostAdminView.view)
async def decline_post(message: Message, state: FSMContext):
    post = await AdminProxyInterface.get_post(state=state)
    await post.delete()

    await message.answer("Пост отклонён.")

    current_post_number = await AdminProxyInterface.get_current_post_number(state=state)
    posts_quantity = await AdminProxyInterface.get_posts_quantity(state=state)
    if current_post_number == posts_quantity:
        current_post_number -= 1

    await view_admin_suggest_post(
        message=message,
        state=state,
        post_number=current_post_number,
        update_posts_quantity=True
    )
