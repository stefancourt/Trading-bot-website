# Generated by Django 4.2.6 on 2024-03-07 00:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_trade_userprofile_delete_funds'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Trade',
            new_name='Trades',
        ),
    ]
