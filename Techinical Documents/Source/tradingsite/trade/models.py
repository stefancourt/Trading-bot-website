from django.db import models

# Create your models here.
class AAPLStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class MSFTStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)



class StockType(models.Model):

    AAPL = 'Apple'
    MSFT = 'Microsoft'

    STOCK_TYPE_CHOICES = [
        (AAPL, 'Apple (AAPL)'),
        (MSFT, 'Microsoft (MSFT)'),
    ]

    stock_type = models.CharField(
    'Stock Type', max_length=15, blank=False, choices=STOCK_TYPE_CHOICES)