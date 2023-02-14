from aiogram.dispatcher.filters.state import State, StatesGroup


class PostAdminView(StatesGroup):
    view = State()
    edit_text = State()
