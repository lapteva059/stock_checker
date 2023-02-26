import asyncio
from tortoise import Tortoise
from db import init_db
from asyncio import sleep
from parser import get_general_data
from updater import update_stock


async def init_db():
    await Tortoise.init(
        db_url='postgres://admin:admin@localhost:5432/tammytanuka',
        modules={'models': ['models']}
    )

    # обновление БД
    while True:
        await update_stock(await get_general_data())
        await asyncio.sleep(30)


async def main():
    await init_db()

if __name__ == '__main__':
    asyncio.run(main())
