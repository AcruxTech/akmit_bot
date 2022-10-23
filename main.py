import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.config.config import load_config 
from app.handlers.common import register_common_handlers
from app.handlers.callbacks import register_callback_handlers

from db.worker import Worker


logger = logging.getLogger(__name__)
config = load_config()
worker = Worker(config.db.__dict__, logger)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Начать работу'),
        BotCommand(command='/help', description='Доступные команды'),
        BotCommand(command='/cancel', description='Отменить команду')
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        filename='bot.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
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