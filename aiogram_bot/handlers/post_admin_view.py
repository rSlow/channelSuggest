from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from FSM.post_add import Start
from FSM.post_admin_view import PostAdminView
from ORM.posts import Post

from bot import dp, bot
from handlers import delete_center_button_message
from keyboads.posts import AdminPostKeyboard
from keyboads.start import StartKeyboard
from templates import render_template
from utils.admin import admin_required


@dp.message_handler(Text(equals=StartKeyboard.Buttons.admin_posts), state=Start.start)
@admin_required(admins_list=bot.admins)
async def view_admin_suggest_post(message: Message,
                                  state: FSMContext,
                                  post_number: int = 1,
                                  update_posts_quantity: bool = True):
    posts_quantity = await Post.get_posts_quantity()

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
            current_post_number=1
        )
    )


dp.register_message_handler(callback=delete_center_button_message, regexp=r"\d+\s[/]\s\d", state=PostAdminView.view)
