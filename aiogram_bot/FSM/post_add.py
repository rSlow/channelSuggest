from aiogram.dispatcher.filters.state import StatesGroup, State


class Start(StatesGroup):
    start = State()
    dice = State()


class AddPost(StatesGroup):
    set_post = State()
    confirm_post = State()
    edit_text = State()
    del_medias = State()
