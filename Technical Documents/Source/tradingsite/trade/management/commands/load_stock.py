import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from trade.models import AAPLStock, MSFTStock, JNJStock, PFEStock, JPMStock, BACStock, AMZNStock, NVDAStock, TSLAStock, METAStock, XOMStock, PEPStock, COSTStock, HDStock, ADBEStock, NKEStock
import yfinance as yf
from pathlib import Path

class Command(BaseCommand):
    help = 'Load data from stock_data file'

    def handle(self, *args, **kwargs):

        datafile = Path(settings.BASE_DIR) / 'stock_data'
        multi_data = yf.download(["AAPL", "MSFT", "JNJ", "PFE", "JPM", "BAC"], period="10y")
        last_price_multi = yf.download(["AMZN", "NVDA", "TSLA", "META", "XOM", "PEP", "COST", "HD", "ADBE", "NKE"], period="1d")

        for stock_name in multi_data["Open"]:
            yf.download([stock_name], period="10y").to_csv(datafile / (stock_name + '_hist.csv'))
        for stock_name in last_price_multi["Open"]:
            yf.download([stock_name], period="2d").to_csv(datafile / (stock_name + '_hist.csv'))

        datafile = settings.BASE_DIR / 'stock_data' / 'AAPL_hist.csv'

        AAPLStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                AAPLStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])
        
        datafile = settings.BASE_DIR / 'stock_data' / 'MSFT_hist.csv'

        MSFTStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                MSFTStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])


        datafile = settings.BASE_DIR / 'stock_data' / 'JNJ_hist.csv'

        JNJStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                JNJStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'PFE_hist.csv'

        PFEStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                PFEStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'JPM_hist.csv'

        JPMStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                JPMStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'BAC_hist.csv'

        BACStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                BACStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])


    
        datafile = settings.BASE_DIR / 'stock_data' / 'AMZN_hist.csv'

        AMZNStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                AMZNStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])


        datafile = settings.BASE_DIR / 'stock_data' / 'NVDA_hist.csv'

        NVDAStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                NVDAStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'TSLA_hist.csv'

        TSLAStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                TSLAStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'META_hist.csv'

        METAStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                METAStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'XOM_hist.csv'

        XOMStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                XOMStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'PEP_hist.csv'

        PEPStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                PEPStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'COST_hist.csv'

        COSTStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                COSTStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'HD_hist.csv'

        HDStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                HDStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'ADBE_hist.csv'

        ADBEStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                ADBEStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])

        datafile = settings.BASE_DIR / 'stock_data' / 'NKE_hist.csv'

        NKEStock.objects.all().delete()
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Creates a stock object for each row in the csv with the following attributes to be used
                NKEStock.objects.get_or_create(date=row['Date'],open=row['Open'],high=row['High'],low=row['Low'],close=row['Close'])