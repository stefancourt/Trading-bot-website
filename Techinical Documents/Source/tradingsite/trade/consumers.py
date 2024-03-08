import json
from asyncio import sleep
from django.db.models import Sum
from trade.models import AAPLStock, MSFTStock
from main.models import UserProfile, Trades
from asgiref.sync import sync_to_async
from django.utils.timezone import make_aware
import datetime
import threading

from channels.generic.websocket import AsyncWebsocketConsumer, StopConsumer


class GraphConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_paused = False  # Initialize a boolean variable to track paused state
        self.end = False

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)

        start = data.get('start')
        stock_type = data.get('stockType')

        user_id = data.get('user_id')
        open_trade = data.get('open_trade')

        if data.get('take_profit'):
            user_id = data.get('user_id')
            open_trade = data.get('open_trade')
            # So that amount_gained is always positive
            amount_gained = abs(data.get('take_profit') - open_trade)
            user_profile = await sync_to_async(UserProfile.objects.get)(user_id=user_id)
            user_profile.money_in_account += amount_gained
            await sync_to_async(user_profile.save)()
            trade = Trades(user_id=user_id, stock_name=stock_type, pnl=amount_gained)
            await sync_to_async(trade.save)()
            all_trades = await sync_to_async(list) (
                Trades.objects.filter(user_id=user_id)
            )
            reversed_all_trades = list(reversed(all_trades))
            # To accumulate total_pnl get last two entries add and save
            reversed_all_trades[0].total_pnl = reversed_all_trades[1].total_pnl + amount_gained
            await sync_to_async(reversed_all_trades[0].save)()








        if data.get('stop_loss'):
            user_id = data.get('user_id')
            open_trade = data.get('open_trade')
            # So that amount_gained is always negative
            amount_lost = abs(open_trade - data.get('stop_loss'))
            user_profile = await sync_to_async(UserProfile.objects.get)(user_id=user_id)
            user_profile.money_in_account -= amount_lost
            await sync_to_async(user_profile.save)()
            trade = Trades(user_id=user_id, stock_name=stock_type, pnl=-amount_lost)
            last_trade = await sync_to_async(Trades.objects.last)()
            last_trade.total_pnl -= amount_lost
            await sync_to_async(last_trade.save)()
            all_trades = await sync_to_async(list) (
                Trades.objects.filter(user_id=user_id)
            )
            reversed_all_trades = list(reversed(all_trades))
            # To accumulate total_pnl get last two entries add and save
            reversed_all_trades[0].total_pnl = reversed_all_trades[1].total_pnl - amount_lost
            await sync_to_async(reversed_all_trades[0].save)()




        if stock_type == "Microsoft":
            msft_stocks = await sync_to_async(list)(
                MSFTStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )  # Check if updates are paused
            if msft_stocks[0].date.isoformat() == start:
                await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "open": msft_stocks[0].open}))  
                await sleep(1)
            else:
                n = 1
                while n < len(msft_stocks):
                    if msft_stocks[0].date.isoformat() == start:
                        await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "open": msft_stocks[0].open}))  
                        await sleep(1)
                        break
                    else:
                        n += 1
                        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
                        start_date += datetime.timedelta(days=1)
                        start = start_date.strftime("%Y-%m-%d")

        elif stock_type == "Apple":
            aapl_stocks = await sync_to_async(list)(
                AAPLStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )
            for stock in aapl_stocks:
                print(stock)
                if not self.is_paused:  # Check if updates are paused
                    await self.send(json.dumps({"date": stock.date.isoformat(), "open": stock.open}))  
                await sleep(1)

    def disconnect(self, event):
        print('websocket disconnected...', event)
        self.end = True
        raise StopConsumer()

    async def pause_graph(self):
        self.is_paused = True

    async def resume_graph(self):
        self.is_paused = False