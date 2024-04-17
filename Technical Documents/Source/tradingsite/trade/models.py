from django.db import models

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

class METAStock(models.Model):
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
        (AAPL, 'Apple'),
        (MSFT, 'Microsoft'),
    ]

    stock_type = models.CharField(
    'Stock Type', max_length=15, blank=False, choices=STOCK_TYPE_CHOICES)