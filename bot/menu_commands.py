from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начало работы'),
        BotCommand(command='/task',
                   description='Выбор задачи'),
        BotCommand(command='/cancel',
                   description='Отмена задачи'),
        BotCommand(command='/stats',
                   description='Статистика за день'),
    ]
    await bot.set_my_commands(main_menu_commands)
