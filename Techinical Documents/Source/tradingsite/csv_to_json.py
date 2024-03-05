import csv
import json
import os

with open('stock_data/AAPL_hist.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

with open('stock_data/AAPL_hist.json', 'w') as jsonfile:
    json.dump(data, jsonfile)