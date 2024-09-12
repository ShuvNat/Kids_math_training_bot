import asyncio
from aiogram import Bot, Dispatcher
from config import Config, load_config
from handlers_users import user_router


async def main():

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(user_router)

    print("Starting polling...")
    await dp.start_polling(bot)


asyncio.run(main())
