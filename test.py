from db import init_db
from models import Stock
from main import update_stock
import asynctest

class StockTestCase(asynctest.TestCase):

    async def setUp(self):
        await init_db()
        test_stock = Stock(title='test', url='url', in_stock=False)
        await test_stock.save()

    async def test_tovar_pomenyalos_nalychie(self):
        await update_stock([{'title': 'test', 'url': 'lolo', 'in_stock': True}])
        test_stock = await Stock.filter(title='test').first()
        assert test_stock.in_stock == True

        # full_row_data_list = [{'title': 'ТЕСТЕР-СТАК "Призванный меч"', 'in_stock': '',
        #   'url': 'https://sigil.me/product/tester-stak-prizvannyy-mech/'},
        #  {'title': 'ТЕСТЕР-СТАК "Клык одиночки"', 'in_stock': '',
        #   'url': 'https://sigil.me/product/tester-stak-klyk-odinochki/'},
        #  {'title': 'ТЕСТЕР-СТАК "Песочные часы"', 'in_stock': '',
        #   'url': 'https://sigil.me/product/tester-stak-pesochnye-chasy/'},
        #  {'title': 'ТЕСТЕР-СТАК "Волчий плащ"', 'in_stock': '',
        #   'url': 'https://sigil.me/product/tester-stak-volchiy-plashch/'},
        #  {'title': 'НАБОР "Светящийся знак"', 'in_stock': '',
        #   'url': 'https://sigil.me/product/nabor-svetyashchiysya-znak/'},
        #  {'title': 'ТЕСТЕР-СТАК "Танец лепестков"', 'in_stock': '',
        #   'url': 'https://sigil.me/product/tester-stak-tanets-lepestkov/'}]