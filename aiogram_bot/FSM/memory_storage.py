from aiogram.contrib.fsm_storage.memory import MemoryStorage

from ORM.states import UserState


class ModifiedMemoryStorage(MemoryStorage):
    async def set_state(self, *,
                        chat: str | int | None = None,
                        user: str | int | None = None,
                        state: bytes | str = None):
        current_state = await self.get_state(
            chat=chat, user=user
        )
        if current_state != state:
            await super(ModifiedMemoryStorage, self).set_state(
                chat=chat,
                user=user,
                state=state
            )
            await UserState.set_state(
                user_id=user,
                state=state
            )

    async def set_all_states(self):
        users = await UserState.get_all_states()
        for user in users:
            await self.set_state(
                chat=user.user_id,
                user=user.user_id,
                state=user.state,
            )
