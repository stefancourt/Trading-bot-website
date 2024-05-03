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

class AMZNStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class NVDAStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class TSLAStock(models.Model):
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

class XOMStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class PEPStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class COSTStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class HDStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class ADBEStock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


    class Meta:
        ordering = ('date',)

class NKEStock(models.Model):
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

class NewsStockType(models.Model):

    AAPL = 'Apple'
    MSFT = 'Microsoft'
    JNJ = 'Jhonson&Jhonson'
    PFE = 'Pfizer'
    BAC = 'BankofAmerica'

    STOCK_TYPE_CHOICES = [
        (AAPL, 'Apple'),
        (MSFT, 'Microsoft'),
        (JNJ, 'Jhonson&Jhonson'),
        (PFE, 'Pfizer'),
        (BAC, 'BankofAmerica'),
        
    ]

    stock_type = models.CharField(
    'Stock Type', max_length=15, blank=False, choices=STOCK_TYPE_CHOICES)