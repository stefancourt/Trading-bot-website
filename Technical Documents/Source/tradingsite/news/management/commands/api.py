import requests
from django.core.management.base import BaseCommand
from django.conf import settings
import json

API_KEY = "7N8C29LEDB288DN7"
AAPL_url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=7N8C29LEDB288DN7'
MSFT_url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=MSFT&apikey=7N8C29LEDB288DN7'
JNJ_url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=JNJ&apikey=7N8C29LEDB288DN7'
PFE_url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=PFE&apikey=7N8C29LEDB288DN7'
BAC_url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=BAC&apikey=7N8C29LEDB288DN7'

class Command(BaseCommand):
    help = 'Write api data to file'

    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'stock_data' / 'news' / 'AAPL_news.json'

        # Sends a request to pull information from alpha vantage api
        r = requests.get(AAPL_url)
        data = r.json()

        # Writes this data to a json file in /stock_data/news/
        with open(datafile, 'w') as f:
            json.dump(data, f)

        datafile = settings.BASE_DIR / 'stock_data' / 'news' / 'MSFT_news.json'

        # Sends a request to pull information from alpha vantage api
        r = requests.get(MSFT_url)
        data = r.json()

        # Writes this data to a json file in /stock_data/news/
        with open(datafile, 'w') as f:
            json.dump(data, f)
        
        datafile = settings.BASE_DIR / 'stock_data' / 'news' / 'JNJ_news.json'

        # Sends a request to pull information from alpha vantage api
        r = requests.get(JNJ_url)
        data = r.json()

        # Writes this data to a json file in /stock_data/news/
        with open(datafile, 'w') as f:
            json.dump(data, f)

        datafile = settings.BASE_DIR / 'stock_data' / 'news' / 'PFE_news.json'

        # Sends a request to pull information from alpha vantage api
        r = requests.get(PFE_url)
        data = r.json()

        # Writes this data to a json file in /stock_data/news/
        with open(datafile, 'w') as f:
            json.dump(data, f)

        datafile = settings.BASE_DIR / 'stock_data' / 'news' / 'BAC_news.json'

        # Sends a request to pull information from alpha vantage api
        r = requests.get(BAC_url)
        data = r.json()

        # Writes this data to a json file in /stock_data/news/
        with open(datafile, 'w') as f:
            json.dump(data, f)