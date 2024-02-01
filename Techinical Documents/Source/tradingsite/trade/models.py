from django.db import models

# Create your models here.
class Stock(models.Model):
    date = models.DateField()
    close = models.FloatField()

    class Meta:
        ordering = ('date', )