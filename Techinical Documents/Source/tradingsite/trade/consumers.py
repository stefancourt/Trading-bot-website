import json
from asyncio import sleep
from trade.models import AAPLStock, MSFTStock
from asgiref.sync import sync_to_async
from django.utils.timezone import make_aware
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer

class GraphConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_paused = False  # Initialize a boolean variable to track paused state

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        start = data.get('start')
        stock_type = data.get('stockType')

        open = data.get('open')
        take_profit = data.get('take_profit')
        stop_loss = data.get('stop_loss')

        if take_profit :
            # So that amount_gained is always positive
            amount_gained = abs(take_profit - open)
        if stop_loss:
            # So that amount_gained is always negative
            amount_gained = -abs(open-stop_loss)

        if stock_type == "Microsoft":
            msft_stocks = await sync_to_async(list)(
                MSFTStock.objects.filter(date__gte=make_aware(datetime.strptime(start, '%Y-%m-%d')))
            )
            for stock in msft_stocks:
                if not self.is_paused:  # Check if updates are paused
                    await self.send(json.dumps({"date": stock.date.isoformat(), "open": stock.open}))  
                await sleep(1)

        elif stock_type == "Apple":
            aapl_stocks = await sync_to_async(list)(
                AAPLStock.objects.filter(date__gte=make_aware(datetime.strptime(start, '%Y-%m-%d')))
            )
            for stock in aapl_stocks:
                if not self.is_paused:  # Check if updates are paused
                    await self.send(json.dumps({"date": stock.date.isoformat(), "open": stock.open}))  
                await sleep(1)

    def disconnect(self, close_code):
        pass

    async def pause_graph(self):
        self.is_paused = True

    async def resume_graph(self):
        self.is_paused = False