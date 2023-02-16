from typing import Any

from aiogram.dispatcher import FSMContext


class ProxyInterface:
    @staticmethod
    async def _get_data(state: FSMContext, key: str, default: Any = None):
        data = await state.get_data()
        try:
            value: Any = data[key]
        except KeyError:
            if default is not None:
                value = default
            else:
                raise
        return value

    @staticmethod
    async def _set_data(state: FSMContext, data: dict):
        new_data = await state.get_data()
        new_data.update(data)
        await state.set_data(data=new_data)
