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
    #Stock.bulk_create([

   # ])
    #stocks = await Stock.all()
    print("Наличие пустой БД")
    #print(stocks)

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

    products_removed_from_shop = stocks_from_db - stocks
    print("Удаленные из магазина товары")
    print(products_removed_from_shop)

    #Удаление из БД товаров, удаленных из магазина
    if products_removed_from_shop:
        removed_products = await Stock.filter(title=products_removed_from_shop.title).all()
        for products_removed_from_shop in removed_products:
            await products_removed_from_shop.delete()

    pass

    print("Товары, появившиеся в наличии")
    for new_stock in stocks & stocks_from_db:
        old_products = await Stock.filter(title=new_stock.title).first()
        if old_products:
            if old_products.in_stock != new_stock.in_stock:
                # все ифы логика сравнения и уведомленпя тут old_stock = new_stock заменяем старые данные на ноыве
                # если не совпадает
                print(old_products)
                old_products.in_stock = new_stock.in_stock
                await old_products.save()
                await old_products.notify_subscribers(new_stock.new_stock_message)
    #print(old_products)
