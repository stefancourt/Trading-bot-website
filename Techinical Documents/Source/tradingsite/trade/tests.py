from django.test import TestCase
from trade.models import AAPLStock
# Create your tests here.

n = 4
aapl_stock = AAPLStock.objects.all()[n]


class StockTestCase(TestCase):
    print(aapl_stock.date)