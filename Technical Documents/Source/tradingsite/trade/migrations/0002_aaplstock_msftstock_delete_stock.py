# Generated by Django 4.2.6 on 2024-03-03 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AAPLStock',
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
            name='MSFTStock',
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
        migrations.DeleteModel(
            name='Stock',
        ),
    ]
