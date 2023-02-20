from models import Stock
from db import init_db

#сохранение в пустую бд
async def save_stock(list_of_raw_stocks):
    await init_db()
    stocks = [Stock(
        title=stock['title'],
        in_stock=False if stock['in_stock'] else True,
        url=stock['url']) for stock in list_of_raw_stocks]
    await Stock.bulk_create(stocks)

#Обновление наличия
async def update_stock(list_of_raw_stocks):
    stocks = {Stock(
        title=stock['title'],
        in_stock=False if stock['in_stock'] else True,
        url=stock['url']) for stock in list_of_raw_stocks}

    #получение товаров из БД
    stocks_from_db = {stock for stock in await Stock.all()}
    #новые товары = спарсенные товары - товары из бд
    new_stocks = stocks - stocks_from_db
    print("Новые товары")
    print(new_stocks)
    # сохранение новых товаров в бд
    await Stock.bulk_create(new_stocks)

    print("Удаленные из магазина товары")
    products_removed_from_shop = stocks_from_db - stocks
    print(products_removed_from_shop)
    if products_removed_from_shop:
        removed_products = await Stock.get(title=products_removed_from_shop.title).first()
        for products_removed_from_shop in removed_products:
            await products_removed_from_shop.delete()

    pass

    print("Товары, появившиеся в наличии")
    old_products_new_stock = []
    for new_stock in stocks & stocks_from_db:
        old_product = await Stock.filter(title=new_stock.title).first()
        if old_product:
            if old_product.in_stock != new_stock.in_stock and old_product.in_stock is False:
                print(old_product)
                old_product.in_stock = new_stock.in_stock
                old_products_new_stock.append(old_product)
                await old_product.save()
                await old_product.notify(new_stock.new_stock_message)
    print(old_products_new_stock)

    print("Товары, ушедшие из наличия")
    old_products_out_of_stock = []
    for out_of_stock in stocks & stocks_from_db:
        old_product = await Stock.filter(title=out_of_stock.title).first()
        if old_product:
            if old_product.in_stock != out_of_stock.in_stock and old_product.in_stock is True:
                print(old_product)
                old_product.in_stock = out_of_stock.in_stock
                old_products_out_of_stock.append(old_product)
                await old_product.save()
                await old_product.notify(new_stock.new_stock_message)
    print (old_products_out_of_stock)