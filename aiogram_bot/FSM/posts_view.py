from aiogram.dispatcher.filters.state import StatesGroup, State


class PostView(StatesGroup):
    view = State()
