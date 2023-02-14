import asyncio
from tortoise import Tortoise
from aiohttp_requests import requests
from bs4 import BeautifulSoup
from models import Stock
from db import init_db
from asyncio import sleep
from datetime import datetime
from parser import get_page_data, get_html, get_total_pages
from updater import save_stock, update_stock

from tortoise.transactions import atomic, in_transaction

async def main():
    await init_db()

    url = 'https://sigil.me/collection/all'
    page_part = '?PAGEN_1='

    full_row_data_list = []
    total_pages = get_total_pages(await get_html(url))

    for i in range(1, total_pages + 1):
        url_gen = url + page_part + str(i)
        stock_row_data_list = get_page_data(await get_html(url_gen))
        # print(full_row_data_list)
        full_row_data_list += stock_row_data_list
    print(full_row_data_list)

    #сохранение в пустую БД
    #await save_stock(full_row_data_list)

    #обновление БД
    await update_stock(full_row_data_list)

if __name__ == '__main__':
    asyncio.run(main())

   # asyncio.run(update_stock())