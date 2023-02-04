import logging

from bot import storage
from ORM.base import stop_database, create_database


async def on_startup(_):
    await create_database()
    await storage.set_all_states()

    try:
        import handlers
    except ImportError as ex:
        logging.warn(msg="[IMPORT ERROR]", exc_info=ex)


async def on_shutdown(_):
    await stop_database()
