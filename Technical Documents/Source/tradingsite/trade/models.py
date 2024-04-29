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

class JNJStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class PFEStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class JPMStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class BACStock(models.Model):
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
    JNJ = 'Jhonson&Jhonson'
    PFE = 'Pfizer'
    JPM = 'JPMorgan'
    BAC = 'BankofAmerica'

    STOCK_TYPE_CHOICES = [
        (AAPL, 'Apple'),
        (MSFT, 'Microsoft'),
        (JNJ, 'Jhonson&Jhonson'),
        (PFE, 'Pfizer'),
        (JPM, 'JPMorgan'),
        (BAC, 'BankofAmerica'),
        
    ]

    stock_type = models.CharField(
    'Stock Type', max_length=15, blank=False, choices=STOCK_TYPE_CHOICES)