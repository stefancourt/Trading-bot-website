from django.db import models

# Create your models here.
class Stock(models.Model):
    date = models.DateField()
    close = models.FloatField()

    class Meta:
        ordering = ('date',)

class StockType(models.Model):

    AAPL = 'AAPL_hist.csv'
    MSFT = 'MSFT_hist.csv'

    STOCK_TYPE_CHOICES = [
        (AAPL, 'Apple (AAPL)'),
        (MSFT, 'Microsoft (MSFT)'),
    ]

    stock_type = models.CharField(
    'Stock Type', max_length=15, blank=False, choices=STOCK_TYPE_CHOICES)