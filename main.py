import asyncio
from tortoise import Tortoise
from aiogram import executor

from parser import get_general_data
from updater import update_stock
from tg_bot.tg_bot import dp


async def init_db():
    await Tortoise.init(
        db_url='postgres://admin:admin@localhost:5432/tammytanuka',
        modules={'models': ['models']}
    )

    # обновление БД
    while True:
        await update_stock(await get_general_data())
        await asyncio.sleep(3)


async def main():
    await init_db()

if __name__ == '__main__':
    #asyncio.run(main())
    dp.loop.create_task(main())
    executor.start_polling(dp, skip_updates=True)
