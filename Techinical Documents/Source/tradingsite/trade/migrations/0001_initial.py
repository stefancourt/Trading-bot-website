# Generated by Django 4.2.6 on 2024-03-03 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='StockType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_type', models.CharField(choices=[('AAPL_hist.csv', 'Apple (AAPL)'), ('MSFT_hist.csv', 'Microsoft (MSFT)')], max_length=15, verbose_name='Stock Type')),
            ],
        ),
    ]
