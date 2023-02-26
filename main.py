import asyncio
from tortoise import Tortoise
from aiohttp_requests import requests
from bs4 import BeautifulSoup
from models import Stock
from db import init_db
from asyncio import sleep
from datetime import datetime
from parser import get_page_data, get_html, get_total_pages, get_all_links
from updater import update_stock
from multiprocessing import Pool

from tortoise.transactions import atomic, in_transaction

async def main():
    await init_db()

    url = 'https://sigil.me/collection/all'
    page_part = '?PAGEN_1='

    url_eggs = 'https://sigil.me/collection/sigil-eggs/'
    url_adventures = 'https://sigil.me/collection/sigil-adventures/'

    full_row_data_list = []
    all_links = []
    total_pages = get_total_pages(await get_html(url))
    for i in range(1, total_pages + 1):
        url_gen = url + page_part + str(i)
        links = get_all_links(await get_html(url_gen))
        all_links += links

    print(all_links)
    for link in all_links:
        stock_row_data_list = get_page_data(await get_html(link), link)
        full_row_data_list += stock_row_data_list

    #обновление БД
    await update_stock(full_row_data_list)

if __name__ == '__main__':
    asyncio.run(main())