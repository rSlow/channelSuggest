import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from FSM.post_add import Start

from FSM.posts_view import PostView
from ORM.posts import Post
from bot import dp
from handlers import start
from keyboads.posts import UserPostKeyboard
from keyboads.start import StartKeyboard
from utils.post_processors import compile_post_message
from utils.post_proxy import (init_posts_quantity_and_current,
                              get_posts_quantity,
                              get_current_post_number,
                              set_post_in_proxy,
                              get_view_post_from_proxy)


@dp.message_handler(Text(equals=StartKeyboard.Buttons.posts), state=Start.start)
async def view_user_post(message: Message,
                         state: FSMContext,
                         post_number: int = 1,
                         update_posts_quantity: bool = True):
    await init_posts_quantity_and_current(
        state=state,
        user_id=message.from_user.id,
        current_post=post_number,
        update_posts_quantity=update_posts_quantity
    )
    posts_quantity = await get_posts_quantity(
        state=state,
    )

    if posts_quantity == 0:
        await start(
            message=message,
            answer="Ваших постов нет в очереди."
        )
    else:
        await PostView.view.set()
        user_post = await Post.get_user_post(
            user_id=message.from_user.id,
            post_number=post_number
        )
        await set_post_in_proxy(
            state=state,
            post=user_post
        )

        if not user_post.medias:
            await message.answer(
                text=user_post.text,
                reply_markup=UserPostKeyboard(
                    current_post_number=post_number,
                    posts_quantity=posts_quantity
                )
            )
        else:
            post_message = await compile_post_message(
                post=user_post
            )
            await message.answer_media_group(
                media=post_message
            )
            # service message to add keyboard
            await message.answer(
                text="service",
                reply_markup=UserPostKeyboard(
                    current_post_number=post_number,
                    posts_quantity=posts_quantity
                )
            )


@dp.message_handler(regexp=r"\d+\s[/]\s\d", state=PostView.view)
async def delete_center_button_message(message: Message):
    await message.delete()


@dp.message_handler(Text(equals=UserPostKeyboard.Buttons.previous), state=PostView.view)
async def get_previous_post(message: Message, state: FSMContext):
    previous_post_number = await get_current_post_number(state=state) - 1

    if previous_post_number == 0:
        await message.delete()
        warning_message = await message.answer(
            text="Не надо так делать больше. Нажимаем только на кнопочки."
        )
        await asyncio.sleep(2)
        await warning_message.delete()
    else:
        await view_user_post(
            message=message,
            state=state,
            post_number=previous_post_number,
            update_posts_quantity=False
        )


@dp.message_handler(Text(equals=UserPostKeyboard.Buttons.next), state=PostView.view)
async def get_next_post(message: Message, state: FSMContext):
    next_post_number = await get_current_post_number(state=state) + 1
    posts_quantity = await get_posts_quantity(state=state)

    if next_post_number > posts_quantity:
        await message.delete()
        warning_message = await message.answer(
            text="Не надо так делать больше. Нажимаем только на кнопочки."
        )
        await asyncio.sleep(2)
        await warning_message.delete()
    else:
        await view_user_post(
            message=message,
            state=state,
            post_number=next_post_number,
            update_posts_quantity=False
        )


@dp.message_handler(Text(equals=UserPostKeyboard.Buttons.delete), state=PostView.view)
async def get_delete_post(message: Message, state: FSMContext):
    current_post_number = await get_current_post_number(state=state)
    posts_quantity = await get_posts_quantity(state=state)
    if current_post_number == posts_quantity:
        current_post_number -= 1

    current_post = await get_view_post_from_proxy(
        state=state
    )
    await Post.delete(current_post)
    await view_user_post(
        message=message,
        state=state,
        post_number=current_post_number
    )
