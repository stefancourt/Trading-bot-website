import requests
from django.core.management.base import BaseCommand
from django.conf import settings
import json

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