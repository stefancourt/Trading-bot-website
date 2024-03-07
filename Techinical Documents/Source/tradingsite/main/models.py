from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Trades(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trade_info = models.CharField(max_length=255)
    # You can add more fields to represent trade information such as trade date, trade type, etc.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money_in_account = models.FloatField(default=1000.00)
    # You can add more fields if needed

    def __str__(self):
        return self.user.username