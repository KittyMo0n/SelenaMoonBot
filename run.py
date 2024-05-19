import asyncio
import logging

from aiogram import Bot, Dispatcher

from share import TOKEN
from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main() # условно асинхронно запускаем операции с базой данных в каждом цикле event loop
    bot = Bot(token=TOKEN) # создаем экземляр класса Bot, кладем в него API ключ для работы с серверами телеграмма
    dp = Dispatcher() # создаем экземляр класса Диспетчер, который обрабатывает события (get request to telegram API)
    dp.include_router(router) # в область диспатчера включаем роутерс
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main()) # event loop
    except KeyboardInterrupt:
        print('Exit')