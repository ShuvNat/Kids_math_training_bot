import asyncio
import sys

from aiogram import Bot, Dispatcher
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import Config, load_config
from db_models import Base
from handlers_users import user_router
from menu_commands import set_main_menu
from middelwares import DbSessionMiddleware, TrackAllUsersMiddleware


async def main():

    config: Config = load_config()

    engine = create_async_engine(
        url=str(config.db.dns),
        echo=config.db.is_echo
    )

    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    dp = Dispatcher(admin_ids=config.tg_bot.admin_ids)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))
    dp.message.outer_middleware(TrackAllUsersMiddleware())

    dp.include_router(user_router)
    bot = Bot(token=config.tg_bot.token)
    dp.startup.register(set_main_menu)

    print("Starting polling...")
    await dp.start_polling(bot)

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
