import os
import asyncio
import logging

from locale import setlocale, LC_TIME
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from common.variables import worker, logger, config
from app.handlers.commands import register_common_handlers
from app.handlers.callbacks import register_callback_handlers


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Начать работу'),
        BotCommand(command='/me', description='Профиль'),
        BotCommand(command='/group', description='Данные о группе'),
        BotCommand(command='/invite', description='Пригласить новых участников'),
        BotCommand(command='/add', description='Добавить д/з'),
        BotCommand(command='/get', description='Посмотреть д/з'),
        BotCommand(command='/help', description='Доступные команды'),
        BotCommand(command='/cancel', description='Отменить команду')
    ]
    await bot.set_my_commands(commands)


async def main():
    setlocale(LC_TIME, 'ru')

    # Удаляем старые логи, если они есть
    if(os.path.isfile('bot.log')):
        os.remove('bot.log')

    # Настройка логирования в stdout
    logging.basicConfig(
        filename='bot.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        encoding='utf-8'
    )
    logger.info('Starting bot')

    # Создание таблиц
    worker.create_all()

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    print((await bot.get_me()).username)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Регистрация хэндлеров
    register_common_handlers(dp)   
    register_callback_handlers(dp)  

    # Установка команд бота     
    await set_commands(bot) 

    # Запуск поллинга                    
    await dp.start_polling()                    


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
