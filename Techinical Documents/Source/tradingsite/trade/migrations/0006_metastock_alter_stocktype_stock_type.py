# Generated by Django 4.2.6 on 2024-04-14 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0005_alter_stocktype_stock_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='METAStock',
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
        migrations.AlterField(
            model_name='stocktype',
            name='stock_type',
            field=models.CharField(choices=[('Apple', 'Apple'), ('Microsoft', 'Microsoft')], max_length=15, verbose_name='Stock Type'),
        ),
    ]
