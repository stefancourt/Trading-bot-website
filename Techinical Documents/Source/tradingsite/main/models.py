from django.db import models

# Create your models here.
class Funds(models.Model):
    credit = models.DecimalField(max_digits=20, decimal_places=2, default=1000)