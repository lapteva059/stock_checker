from models import Stock
from db import init_db


# Обновление наличия
async def update_stock(list_of_raw_stocks):
    stocks = {Stock(
        title=stock['title'],
        in_stock=False if stock['in_stock'] else True,
        url=stock['url']) for stock in list_of_raw_stocks}

    # получение товаров из БД
    stocks_from_db = {stock for stock in await Stock.all()}
    # новые товары = спарсенные товары - товары из бд
    new_products = stocks - stocks_from_db
    print("Новые товары")
    print(new_products)
    # сохранение новых товаров в бд
    await Stock.bulk_create(new_products)
    # оповещение
    if new_products:
        for new_product in new_products:
            await new_products.notify_subscribers(new_product.new_stock_message)

    print("Удаленные из магазина товары")
    products_removed_from_shop = stocks_from_db - stocks
    print(products_removed_from_shop)
    if products_removed_from_shop:
        for removed_product in products_removed_from_shop:
            await Stock.get(title=removed_product.title).first().delete()

    pass

    # Изменение наличия
    old_products_new_stock = {}
    old_products_out_of_stock = {}
    for new_stock in stocks_from_db & stocks:
        old_product = await Stock.get(title=new_stock.title).first()
        if old_product:
            if new_stock.in_stock != old_product.in_stock:
                if old_product.in_stock is False:
                    old_products_new_stock.add(old_product)
                else:
                    old_products_out_of_stock.add(old_product)
            old_product.in_stock = new_stock.in_stock
            await old_product.save()
    print(old_products_new_stock)
    if old_products_new_stock:
        for new_product in old_products_new_stock:
            await new_product.notify_subscribers(new_product.new_stock_message)

    print("Товары, появившиеся в наличии")
    print(old_products_new_stock)
    print("Товары, ушедшие из наличия")
    print(old_products_out_of_stock)

