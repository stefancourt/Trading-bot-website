import json
from asyncio import sleep
from trade.models import AAPLStock, MSFTStock
from main.models import UserProfile, Trades
from asgiref.sync import sync_to_async
from django.utils.timezone import make_aware
import datetime
import pandas as pd
import numpy as np
import os

from channels.generic.websocket import AsyncWebsocketConsumer, StopConsumer

# Calculate moving averages
def moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

# Calculate momentum
def momentum(data, window):
    return data['Close'].diff(window - 1)

# Calculate VWAP
def vwap(data):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    volume_price = typical_price * data['Volume']
    cumulative_volume = data['Volume'].cumsum()
    cumulative_volume_price = volume_price.cumsum()
    return cumulative_volume_price / cumulative_volume

# Trading strategy combining moving average crossover, momentum, and VWAP
def trading_strategy(data, short_window, long_window, momentum_window, ma_bool=False, vwap_bool=False, momentum_bool=False):
    signals = pd.DataFrame(index=data.index)
    signals['Date'] = pd.to_datetime(data['Date'])
    signals['signal'] = 0.0

    # Moving average crossover
    if ma_bool == True:
        signals['short_mavg'] = moving_average(data, short_window)
        signals['long_mavg'] = moving_average(data, long_window)
        signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, -1.0)

    # Momentum
    if momentum_bool == True:
        signals['momentum'] = momentum(data, momentum_window)
        signals['signal'][(signals['momentum'] > 0) & (signals['signal'] != 0)] = 1.0
        signals['signal'][(signals['momentum'] < 0) & (signals['signal'] != 0)] = -1.0

    # VWAP
    if vwap_bool == True:
        vwap_values = vwap(data)
        signals['vwap'] = vwap_values.shift(1)
        signals['signal'][data['Close'] > signals['vwap']] = 1.0
        signals['signal'][data['Close'] < signals['vwap']] = -1.0

    return signals

class GraphConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        global first_pass
        first_pass = True
        self.unique_id = self.scope["query_string"].decode("utf-8")
        await self.accept()

    async def receive(self, text_data):
        global first_pass
        data = json.loads(text_data)

        ai_type = data.get('aiType')
        start = data.get('start')
        stock_type = data.get('stockType')
        amount = data.get('amount')

        user_id = data.get('user_id')
        close_trade = data.get('close_trade')

        if data.get('take_profit'):
            user_id = data.get('user_id')
            close_trade = data.get('close_trade')
            percentage = float(amount)/close_trade
            # So that amount_gained is always positive
            amount_gained = abs(data.get('take_profit') - close_trade) * percentage
            user_profile = await sync_to_async(UserProfile.objects.get)(user_id=user_id)
            user_profile.money_in_account += amount_gained
            await sync_to_async(user_profile.save)()
            # Creates a trade object and saves it to the model
            trade = Trades(user_id=user_id, stock_name=stock_type, pnl=amount_gained)
            await sync_to_async(trade.save)()
            # Finds all trades associated with the user logged in
            all_trades = await sync_to_async(list) (
                Trades.objects.filter(user_id=user_id)
            )
            reversed_all_trades = list(reversed(all_trades))
            # To accumulate total_pnl get last two entries add and save
            try:
                reversed_all_trades[0].total_pnl = reversed_all_trades[1].total_pnl + amount_gained
            except:
                reversed_all_trades[0].total_pnl = amount_gained
            await sync_to_async(reversed_all_trades[0].save)()

        if data.get('stop_loss'):
            user_id = data.get('user_id')
            close_trade = data.get('close_trade')
            percentage = float(amount)/close_trade
            # So that amount_gained is always negative
            amount_lost = abs(close_trade - data.get('stop_loss')) * percentage
            user_profile = await sync_to_async(UserProfile.objects.get)(user_id=user_id)
            user_profile.money_in_account -= amount_lost
            await sync_to_async(user_profile.save)()
            # Creates a trade object and saves it to the model
            trade = Trades(user_id=user_id, stock_name=stock_type, pnl=-amount_lost)
            await sync_to_async(trade.save)()
            # Finds all trades associated with the user logged in
            all_trades = await sync_to_async(list) (
                Trades.objects.filter(user_id=user_id)
            )
            reversed_all_trades = list(reversed(all_trades))
            # To accumulate total_pnl get last two entries add and save
            try:
                reversed_all_trades[0].total_pnl = reversed_all_trades[1].total_pnl - amount_lost
            except:
                reversed_all_trades[0].total_pnl = -amount_lost
            await sync_to_async(reversed_all_trades[0].save)()


        if stock_type == "Microsoft":
            first_date = await sync_to_async(MSFTStock.objects.first)()
            last_date = await sync_to_async(MSFTStock.objects.last)()
            # If date entered is before start or after last date, allow javascript to pick up error
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() < first_date.date:
                await self.send(json.dumps({'first_date': first_date.date.isoformat()}))
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() > last_date.date:
                await self.send(json.dumps({'last_date': last_date.date.isoformat()}))
            # Creates a file in stock_data/signals/ for the signals the websocket is using
            if first_pass:
                df = pd.read_csv("stock_data/MSFT_hist.csv")
                # Start the file from the start date selected
                df = df[df['Date'] >= start]
                # Generates in the file the strategy selected
                if ai_type == "ma":
                    signals = trading_strategy(df, short_window=50, long_window=200, momentum_window=5, ma_bool=True, vwap_bool=False, momentum_bool=False)
                elif ai_type == "vwap":
                    signals = trading_strategy(df, short_window=50, long_window=200, momentum_window=5, ma_bool=False, vwap_bool=True, momentum_bool=False)
                elif ai_type == "momentum":
                    signals = trading_strategy(df, short_window=50, long_window=200, momentum_window=5, ma_bool=False, vwap_bool=False, momentum_bool=True)
                else:
                    signals = trading_strategy(df, short_window=50, long_window=200, momentum_window=5, ma_bool=True, vwap_bool=True, momentum_bool=True)
                signals.to_csv(f"stock_data/signals/{self.unique_id}_signal.csv")
                # Only on first pass
                first_pass=False
            dataframe = pd.read_csv(f"stock_data/signals/{self.unique_id}_signal.csv")
            msft_stocks = await sync_to_async(list)(
                MSFTStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )
            if msft_stocks[0].date.isoformat() == start:
                row = dataframe.loc[dataframe['Date'] == start]
                if data.get('take_profit') or data.get("stop_loss"):
                    # Sends the user's balance to change in the page dynamically
                    await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "close": msft_stocks[0].close, "signal": row["signal"].values[0], "money_in_account": user_profile.money_in_account}))
                else:
                    await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "close": msft_stocks[0].close, "signal": row["signal"].values[0]}))
                await sleep(1)
            else:
                n = 1
                # Loop is needed as some days are not available in the dataset
                while n < len(msft_stocks):
                    if msft_stocks[0].date.isoformat() == start:
                        row = dataframe.loc[dataframe['Date'] == start]
                        if data.get('take_profit') or data.get("stop_loss"):
                            # Sends the user's balance to change in the page dynamically
                            await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "close": msft_stocks[0].close, "signal": row["signal"].values[0], "money_in_account": user_profile.money_in_account}))
                        else:
                            await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "close": msft_stocks[0].close, "signal": row["signal"].values[0]}))
                        await sleep(1)
                        break
                    else:
                        # Changes the start date to one day ahead
                        n += 1
                        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
                        start_date += datetime.timedelta(days=1)
                        start = start_date.strftime("%Y-%m-%d")







        elif stock_type == "Apple":
            first_date = await sync_to_async(AAPLStock.objects.first)()
            last_date = await sync_to_async(AAPLStock.objects.last)()
            # If date entered is before start or after last date, allow javascript to pick up error
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() < first_date.date:
                await self.send(json.dumps({'first_date': first_date.date.isoformat()}))
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() > last_date.date:
                await self.send(json.dumps({'last_date': last_date.date.isoformat()}))
            # Creates a file in stock_data/signals/ for the signals the websocket is using
            if first_pass:
                df = pd.read_csv("stock_data/AAPL_hist.csv")
                # Start the file from the start date selected
                df = df[df['Date'] >= start]
                # Generates in the file the strategy selected
                if ai_type == "ma":
                    signals = trading_strategy(df, short_window=50, long_window=200, momentum_window=5, ma_bool=True, vwap_bool=False, momentum_bool=False)
                elif ai_type == "vwap":
                    signals = trading_strategy(df, short_window=50, long_window=200, momentum_window=5, ma_bool=False, vwap_bool=True, momentum_bool=False)
                elif ai_type == "momentum":
                    signals = trading_strategy(df, short_window=50, long_window=200, momentum_window=5, ma_bool=False, vwap_bool=False, momentum_bool=True)
                else:
                    signals = trading_strategy(df, short_window=50, long_window=200, momentum_window=5, ma_bool=True, vwap_bool=True, momentum_bool=True)
                signals.to_csv(f"stock_data/signals/{self.unique_id}_signal.csv")
                # Only on first pass
                first_pass=False
            dataframe = pd.read_csv(f"stock_data/signals/{self.unique_id}_signal.csv")
            aapl_stocks = await sync_to_async(list)(
                AAPLStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )
            if aapl_stocks[0].date.isoformat() == start:
                row = dataframe.loc[dataframe['Date'] == start]
                if data.get('take_profit') or data.get("stop_loss"):
                    # Sends the user's balance to change in the page dynamically
                    await self.send(json.dumps({"date": aapl_stocks[0].date.isoformat(), "close": aapl_stocks[0].close, "signal": row["signal"].values[0], "money_in_account": user_profile.money_in_account}))
                else:
                    await self.send(json.dumps({"date": aapl_stocks[0].date.isoformat(), "close": aapl_stocks[0].close, "signal": row["signal"].values[0]}))
                await sleep(1)
            else:
                n = 1
                # Loop is needed as some days are not available in the dataset
                while n < len(aapl_stocks):
                    if aapl_stocks[0].date.isoformat() == start:
                        row = dataframe.loc[dataframe['Date'] == start]
                        if data.get('take_profit') or data.get("stop_loss"):
                            # Sends the user's balance to change in the page dynamically
                            await self.send(json.dumps({"date": aapl_stocks[0].date.isoformat(), "close": aapl_stocks[0].close, "signal": row["signal"].values[0], "money_in_account": user_profile.money_in_account}))
                        else:
                            await self.send(json.dumps({"date": aapl_stocks[0].date.isoformat(), "close": aapl_stocks[0].close, "signal": row["signal"].values[0]}))
                        await sleep(1)
                        break
                    else:
                        # Changes the start date to one day ahead
                        n += 1
                        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
                        start_date += datetime.timedelta(days=1)
                        start = start_date.strftime("%Y-%m-%d")

    def disconnect(self, event):
        print("WebSocket disconnected with unique ID:", self.unique_id)
        os.remove(f'stock_data/signals/{self.unique_id}_signal.csv')
        self.end = True
        raise StopConsumer()