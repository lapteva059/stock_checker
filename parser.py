import asyncio
from aiohttp_requests import requests
from bs4 import BeautifulSoup

async def get_html(url):
    r = await requests.get(url)
    text = await r.text()
    return text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    total_pages = soup.find('div', class_='col').find_all('li', class_='pagination-item')[-2].text
    # print(total_pages)
    return int(total_pages)

def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('div', class_='mb-4 catalog-section').find_all('div', class_='product-item-small-card')
    # print(len(ads))
    stock_row_data_list = []

    for ad in ads:
        try:
            title = ad.find('div', class_='card-title').text.strip()
            # print(title)
        except:
            title = ''

        try:
            if ad.find('div', class_='card-price').find('small', class_='small').text is not None:
                in_stock = ad.find('div', class_='card-price').find('small', class_='small').text.split('\ ')[1]
                # print(in_stock)
            else:
                in_stock = ''
        except:
            in_stock = ''

        try:
            url = 'https://sigil.me' + ad.find('div', class_='card-title').find('a').get('href')
            # print(url)
        except:
            url = ''

        row_data = {'title': title,
                    'in_stock': in_stock,
                    'url': url}

        stock_row_data_list.append(row_data)

    return stock_row_data_list