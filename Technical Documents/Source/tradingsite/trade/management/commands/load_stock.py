import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from trade.models import AAPLStock, MSFTStock, METAStock
import yfinance as yf
from pathlib import Path

class Command(BaseCommand):
    help = 'Load data from stock_data file'

    def handle(self, *args, **kwargs):

        datafile = Path(settings.BASE_DIR) / 'stock_data'
        multi_data = yf.download(["AAPL", "MSFT", "JNJ", "PFE", "JPM", "BAC"], period="10y")

        for stock_name in multi_data["Open"]:
            yf.download([stock_name], period="10y").to_csv(datafile / (stock_name + '_hist.csv'))


        datafile = settings.BASE_DIR / 'stock_data' / 'AAPL_hist.csv'

        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates an Apple stock object for each row in the csv with the following attributes to be used
                AAPLStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])
        
        datafile = settings.BASE_DIR / 'stock_data' / 'MSFT_hist.csv'

        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a Microsoft stock object for each row in the csv with the following attributes to be used
                MSFTStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])


        datafile = settings.BASE_DIR / 'stock_data' / 'META_hist.csv'

        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a Microsoft stock object for each row in the csv with the following attributes to be used
                METAStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])