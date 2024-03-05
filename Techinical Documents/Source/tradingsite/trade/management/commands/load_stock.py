import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from trade.models import AAPLStock, MSFTStock

class Command(BaseCommand):
    help = 'Load data from stock_data file'

    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'stock_data' / 'AAPL_hist.csv'

        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # dt = row['date']

                AAPLStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])
        
        datafile = settings.BASE_DIR / 'stock_data' / 'MSFT_hist.csv'

        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # dt = row['date']

                MSFTStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])