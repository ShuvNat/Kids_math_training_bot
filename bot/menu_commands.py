from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начало работы'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/task',
                   description='Выбор задачи'),
        BotCommand(command='/cancel',
                   description='Отмена задачи'),
        BotCommand(command='/stats_daily',
                   description='Статистика за день'),
        BotCommand(command='/stats_weekly',
                   description='Статистика за неделю'),
        BotCommand(command='/stats_monthly',
                   description='Статистика за месяц'),
    ]
    await bot.set_my_commands(main_menu_commands)
