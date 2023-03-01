import asyncio
from tortoise import Tortoise
from aiogram import executor

from parser import get_general_data, get_all_links
from updater import update_stock
import settings
from tg_bot.tg_bot import dp


async def init_db():
    await Tortoise.init(
        db_url=settings.db_url,
        modules={'models': ['models']}
    )

    # обновление БД
async def update():
    while True:
        await update_stock(await get_general_data())
        await asyncio.sleep(3)


async def main():
    await init_db()
    await update()

if __name__ == '__main__':
    dp.loop.create_task(main())
    executor.start_polling(dp, skip_updates=True)
