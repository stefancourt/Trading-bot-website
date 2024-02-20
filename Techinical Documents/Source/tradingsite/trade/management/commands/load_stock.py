import csv
from datetime import datetime
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand
from trade.models import Stock

class Command(BaseCommand):
    help = 'Load data from stock_data file'

    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'stock_data' / 'AAPL_hist.csv'

        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # dt = row['date']

                Stock.objects.get_or_create(date=row['Date'], close=row['Close'])