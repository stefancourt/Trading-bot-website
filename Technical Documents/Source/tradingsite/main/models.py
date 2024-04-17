from django.db import models

from django.contrib.auth.models import User

class Trades(models.Model):
    # Obtains user from django user model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=255)
    pnl = models.FloatField(default=0)
    total_pnl = models.FloatField(default=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money_in_account = models.FloatField(default=1000.00)

    def __str__(self):
        return self.user.username