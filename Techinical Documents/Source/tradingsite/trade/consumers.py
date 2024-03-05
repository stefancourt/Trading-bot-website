import json
from asyncio import sleep
from trade.models import AAPLStock, MSFTStock
from asgiref.sync import sync_to_async
from django.utils.timezone import make_aware
from datetime import datetime


from channels.generic.websocket import AsyncWebsocketConsumer




class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        n = 0
        await self.accept()
        
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        start = data.get('start')
        stock_type = data.get('stockType')
        if stock_type == "Microsoft":
            msft_stocks = await sync_to_async(list)(
                MSFTStock.objects.filter(date__gte=make_aware(datetime.strptime(start, '%Y-%m-%d')))
            )
            for stock in msft_stocks:
                await self.send(json.dumps({"date": stock.date.isoformat(), "open": stock.open}))  # Sending asynchronously
                await sleep(1)
        elif stock_type == "Apple":
            aapl_stocks = await sync_to_async(list)(
                AAPLStock.objects.filter(date__gte=make_aware(datetime.strptime(start, '%Y-%m-%d')))
            )
            for stock in aapl_stocks:
                await self.send(json.dumps({"date": stock.date.isoformat(), "open": stock.open}))  # Sending asynchronously
                await sleep(1)

    

    def disconnect(self, close_code):
        # No need to do anything here, but you could perform cleanup tasks if needed
        pass