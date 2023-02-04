from aiogram.dispatcher.filters.state import StatesGroup, State


class Start(StatesGroup):
    start = State()
    dice = State()


class AddPost(StatesGroup):
    set_post = State()
    add_post = State()
