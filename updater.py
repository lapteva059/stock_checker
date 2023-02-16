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
        old_product = await Stock.filter(title=new_stock.title).first()
        if old_product:
            if old_product.in_stock != new_stock.in_stock:
                print(old_product)
                old_product.in_stock = new_stock.in_stock
                await old_product.save()
                await old_product.notify(new_stock.new_stock_message)
    #print(old_products)


    #товары, ушедшие из наличия
    #поменять "true@/"нет в наличии" в иф
    for new_stock in stocks & stocks_from_db:
        sold_out = await Stock.filter(title=new_stock.title).first()
        if sold_out:
            if sold_out.in_stock != new_stock.in_stock:
                print(sold_out)
                sold_out.in_stock = new_stock.in_stock
                await sold_out.save()