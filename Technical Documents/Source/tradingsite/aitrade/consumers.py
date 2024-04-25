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
def moving_average(data, span):
    return data['Close'].ewm(span=span, adjust=False).mean()
    # return data['Close'].rolling(window=span).mean()

# Calculate RSI
def calculate_rsi(data, window):
    delta = data['Close'].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Calculate ADX
def calculate_adx(data, window):

    # True Range
    data['tr0'] = abs(data['High'] - data['Low'])
    data['tr1'] = abs(data['High'] - data['Close'].shift())
    data['tr2'] = abs(data['Low'] - data['Close'].shift())
    data['TR'] = data[['tr0', 'tr1', 'tr2']].max(axis=1)

    # Directional Movement
    data['DM+'] = np.where((data['High'] - data['High'].shift()) > (data['Low'].shift() - data['Low']), data['High'] - data['High'].shift(), 0)
    data['DM-'] = np.where((data['Low'].shift() - data['Low']) > (data['High'] - data['High'].shift()), data['Low'].shift() - data['Low'], 0)

    # Smoothed True Range
    data['ATR'] = data['TR'].rolling(window=window).mean()

    # Smoothed Directional Movement
    data['ADM+'] = data['DM+'].rolling(window=window).mean()
    data['ADM-'] = data['DM-'].rolling(window=window).mean()

    # Directional Index
    data['DI+'] = (data['ADM+'] / data['ATR']) * 100
    data['DI-'] = (data['ADM-'] / data['ATR']) * 100

    data['DX'] = abs(data['DI+'] - data['DI-']) / (data['DI+'] + data['DI-']) * 100

    adx_values = data['DX'].rolling(window=window).mean()

    return (adx_values, data['DI+'], data['DI-'])

# Trading strategy combining moving average crossover, RSI and ADX
def trading_strategy(data, complete=False, rsi_window=None, overbought_threshold=None, oversold_threshold=None, adx_window=None, adx_threshold=None, short_window=None, long_window=None):
    signals = pd.DataFrame(index=data.index)
    signals['Date'] = pd.to_datetime(data['Date'])
    signals['signal'] = 0.0

        
    # Moving average crossover
    if short_window:
        signals['short_mavg'] = moving_average(data, short_window)
        signals['long_mavg'] = moving_average(data, long_window)
        signals['signal_ma'] = 0.0
        # Place buy order when short moving average crosses above long moving average
        signals.loc[(signals['short_mavg'].shift(1) < signals['long_mavg'].shift(1)) & (signals['short_mavg'] > signals['long_mavg']), 'signal_ma'] = 1.0

        # Place sell order when short moving average crosses below long moving average
        signals.loc[(signals['short_mavg'].shift(1) > signals['long_mavg'].shift(1)) & (signals['short_mavg'] < signals['long_mavg']), 'signal_ma'] = -1.0

    # Relative Strength Index    
    if rsi_window:
        rsi_values = calculate_rsi(data, window=rsi_window)
        signals['signal_rsi'] = 0.0
        signals['rsi'] = rsi_values
        signals.loc[signals['rsi'] > overbought_threshold, 'signal_rsi'] = -1.0
        signals.loc[signals['rsi'] < oversold_threshold, 'signal_rsi'] = 1.0

    # Average Directional Index
    if adx_window:
        adx_values = calculate_adx(data, window=adx_window)
        signals['signal_adx'] = 0.0
        signals['adx'] = adx_values[0]
        signals['+DI'] = adx_values[1]
        signals['-DI'] = adx_values[2]
        signals.loc[(signals['+DI'].shift(1) < signals['-DI'].shift(1)) & (signals['+DI'] > signals['-DI']) & (signals['adx'] > adx_threshold), 'signal_adx'] = 1.0
    
        # Place sell signal when -DI crosses over +DI and ADX is above the threshold
        signals.loc[(signals['+DI'].shift(1) > signals['-DI'].shift(1)) & (signals['+DI'] < signals['-DI']) & (signals['adx'] > adx_threshold), 'signal_adx'] = -1.0
        
        
    if complete:
        signals_sum = signals['signal_ma'] + signals['signal_rsi'] + signals['signal_adx']
        signals['sum'] = signals_sum
        signals['signal'] = 0.0
        signals.loc[signals['sum'] >= 2.0, 'signal'] = 1.0
        signals.loc[signals['sum'] <= -2.0, 'signal'] = -1.0
            
    elif short_window:
        signals['signal'] = signals['signal_ma']
    elif rsi_window:
        signals['signal'] = signals['signal_rsi']
    elif adx_window:
        signals['signal'] = signals['signal_adx']
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
                    signals = trading_strategy(df, short_window=10, long_window=30,) # tp = 0.2
                elif ai_type == "adx":
                    signals = trading_strategy(df, adw_window=10, adx_threshold=25) # tp = 0.2
                elif ai_type == "rsi":
                    signals = trading_strategy(df, rsi_window=100, overbought_threshold=90, oversold_threshold=60)# 0.2
                else:
                    signals = trading_strategy(df, complete=True, short_window=5, long_window=10, adx_window=14, adx_threshold=25, rsi_window=70, overbought_threshold=70, oversold_threshold=60) # tp = 0.2
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
                    signals = trading_strategy(df, short_window=10, long_window=30,) # tp = 0.2
                elif ai_type == "adx":
                    signals = trading_strategy(df, adw_window=10, adx_threshold=25) # tp = 0.2
                elif ai_type == "rsi":
                    signals = trading_strategy(df, rsi_window=100, overbought_threshold=90, oversold_threshold=60) # tp = 0.2
                else:
                    signals = trading_strategy(df, complete=True, short_window=5, long_window=10, adx_window=14, adx_threshold=25, rsi_window=70, overbought_threshold=70, oversold_threshold=60) # tp = 0.2
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