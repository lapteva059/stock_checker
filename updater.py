from models import Stock


# сохранение новых товаров в бд
async def save_new_products(new_products):
    await Stock.bulk_create(new_products)
    # оповещение
    if new_products:
        for new_product in new_products:
            new_product_in_shop = await Stock.get(title=new_product.title).first()
            if new_product_in_shop.in_stock is False:
                await new_product_in_shop.notify_subscribers(new_product_in_shop.new_product_message)
            else:
                await new_product_in_shop.notify_subscribers(new_product_in_shop.new_stock_message)


#Удаление из БД
async def delete_products(products_removed_from_shop):
    print("Удаленные из магазина товары")
    print(products_removed_from_shop)
    if products_removed_from_shop:
        for removed_product in products_removed_from_shop:
            await Stock.get(title=removed_product.title).first().delete()


# Изменение наличия
async def update_products_info(general_stocks):
    old_products_new_stock = set()
    old_products_out_of_stock = set()
    for new_stock in general_stocks:
        old_product = await Stock.get(title=new_stock.title).first()
        if old_product:
            if new_stock.in_stock != old_product.in_stock:
                if old_product.in_stock is False:
                    old_products_new_stock.add(old_product)
                else:
                    old_products_out_of_stock.add(old_product)
            old_product.in_stock = new_stock.in_stock
            await old_product.save()
    # оповещение
    if old_products_new_stock:
        for product_in_stock in old_products_new_stock:
            await product_in_stock.notify_subscribers(product_in_stock.new_stock_message)

    print("Товары, появившиеся в наличии")
    print(old_products_new_stock)
    print("Товары, ушедшие из наличия")
    print(old_products_out_of_stock)


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
    await save_new_products(new_products)
    products_removed_from_shop = stocks_from_db - stocks
    await delete_products(products_removed_from_shop)
    general_stocks = stocks_from_db & stocks
    await update_products_info(general_stocks)

