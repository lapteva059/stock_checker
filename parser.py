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
    return int(total_pages)

def get_all_links(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('div', class_='mb-4 catalog-section').find_all('div', class_='product-item-small-card')
    for ad in ads:
        url = 'https://sigil.me' + ad.find('div', class_='card-title').find('a').get('href')
        links.append(url)
    return links

def get_stock(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('a', class_='btn btn-link product-item-detail-buy-button')
    try:
        if data.get('style') == "display: ;":
            in_stock = data.text.strip()
        else:
            in_stock = ''
    except:
        in_stock = ''
    #print(in_stock)
    return in_stock

def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1', class_='product-title').text.strip()
    # print(in_stock)
    return title

def get_page_data(html, url):
    stock_row_data_list = []
    row_data = {'title': get_title(html),
                'in_stock': get_stock(html),
                'url': url}

    stock_row_data_list.append(row_data)
    print(stock_row_data_list)
    return stock_row_data_list
