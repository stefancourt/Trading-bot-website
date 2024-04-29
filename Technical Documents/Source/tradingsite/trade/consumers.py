import json
from asyncio import sleep
from trade.models import AAPLStock, MSFTStock, JNJStock, JPMStock, PFEStock, BACStock
from main.models import UserProfile, Trades
from asgiref.sync import sync_to_async
from django.utils.timezone import make_aware
import datetime

from channels.generic.websocket import AsyncWebsocketConsumer, StopConsumer


class GraphConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)

        start = data.get('start')
        stock_type = data.get('stockType')

        user_id = data.get('user_id')
        amount = data.get('amount')
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
            msft_stocks = await sync_to_async(list)(
                MSFTStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )
            if msft_stocks[0].date.isoformat() == start:
                if data.get('take_profit') or data.get("stop_loss"):
                    await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "close": msft_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                else:
                    await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "close": msft_stocks[0].close}))
                await sleep(1)
            else:
                n = 1
                # Loop is needed as some days are not available in the dataset
                while n < len(msft_stocks):
                    if msft_stocks[0].date.isoformat() == start:
                        if data.get('take_profit') or data.get("stop_loss"):
                            # Sends the user's balance to change in the page dynamically
                            await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "close": msft_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                        else:
                            await self.send(json.dumps({"date": msft_stocks[0].date.isoformat(), "close": msft_stocks[0].close}))
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
            aapl_stocks = await sync_to_async(list)(
                AAPLStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )
            if aapl_stocks[0].date.isoformat() == start:
                if data.get('take_profit') or data.get("stop_loss"):
                    # Sends the user's balance to change in the page dynamically
                    await self.send(json.dumps({"date": aapl_stocks[0].date.isoformat(), "close": aapl_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                else:
                    await self.send(json.dumps({"date": aapl_stocks[0].date.isoformat(), "close": aapl_stocks[0].close}))
                await sleep(1)
            else:
                n = 1
                # Loop is needed as some days are not available in the dataset
                while n < len(aapl_stocks):
                    if aapl_stocks[0].date.isoformat() == start:
                        if data.get('take_profit') or data.get("stop_loss"):
                            # Sends the user's balance to change in the page dynamically
                            await self.send(json.dumps({"date": aapl_stocks[0].date.isoformat(), "close": aapl_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                        else:
                            await self.send(json.dumps({"date": aapl_stocks[0].date.isoformat(), "close": aapl_stocks[0].close}))
                        await sleep(1)
                        break
                    else:
                        # Changes the start date to one day ahead
                        n += 1
                        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
                        start_date += datetime.timedelta(days=1)
                        start = start_date.strftime("%Y-%m-%d")

        elif stock_type == "Jhonson&Jhonson":
            first_date = await sync_to_async(JNJStock.objects.first)()
            last_date = await sync_to_async(JNJStock.objects.last)()
            # If date entered is before start or after last date, allow javascript to pick up error
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() < first_date.date:
                await self.send(json.dumps({'first_date': first_date.date.isoformat()}))
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() > last_date.date:
                await self.send(json.dumps({'last_date': last_date.date.isoformat()}))
            jnj_stocks = await sync_to_async(list)(
                JNJStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )
            if jnj_stocks[0].date.isoformat() == start:
                if data.get('take_profit') or data.get("stop_loss"):
                    # Sends the user's balance to change in the page dynamically
                    await self.send(json.dumps({"date": jnj_stocks[0].date.isoformat(), "close": jnj_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                else:
                    await self.send(json.dumps({"date": jnj_stocks[0].date.isoformat(), "close": jnj_stocks[0].close}))
                await sleep(1)
            else:
                n = 1
                # Loop is needed as some days are not available in the dataset
                while n < len(jnj_stocks):
                    if jnj_stocks[0].date.isoformat() == start:
                        if data.get('take_profit') or data.get("stop_loss"):
                            # Sends the user's balance to change in the page dynamically
                            await self.send(json.dumps({"date": jnj_stocks[0].date.isoformat(), "close": jnj_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                        else:
                            await self.send(json.dumps({"date": jnj_stocks[0].date.isoformat(), "close": jnj_stocks[0].close}))
                        await sleep(1)
                        break
                    else:
                        # Changes the start date to one day ahead
                        n += 1
                        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
                        start_date += datetime.timedelta(days=1)
                        start = start_date.strftime("%Y-%m-%d")

        elif stock_type == "Pfizer":
            first_date = await sync_to_async(PFEStock.objects.first)()
            last_date = await sync_to_async(PFEStock.objects.last)()
            # If date entered is before start or after last date, allow javascript to pick up error
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() < first_date.date:
                await self.send(json.dumps({'first_date': first_date.date.isoformat()}))
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() > last_date.date:
                await self.send(json.dumps({'last_date': last_date.date.isoformat()}))
            pfe_stocks = await sync_to_async(list)(
                PFEStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )
            if pfe_stocks[0].date.isoformat() == start:
                if data.get('take_profit') or data.get("stop_loss"):
                    # Sends the user's balance to change in the page dynamically
                    await self.send(json.dumps({"date": pfe_stocks[0].date.isoformat(), "close": pfe_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                else:
                    await self.send(json.dumps({"date": pfe_stocks[0].date.isoformat(), "close": pfe_stocks[0].close}))
                await sleep(1)
            else:
                n = 1
                # Loop is needed as some days are not available in the dataset
                while n < len(pfe_stocks):
                    if pfe_stocks[0].date.isoformat() == start:
                        if data.get('take_profit') or data.get("stop_loss"):
                            # Sends the user's balance to change in the page dynamically
                            await self.send(json.dumps({"date": pfe_stocks[0].date.isoformat(), "close": pfe_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                        else:
                            await self.send(json.dumps({"date": pfe_stocks[0].date.isoformat(), "close": pfe_stocks[0].close}))
                        await sleep(1)
                        break
                    else:
                        # Changes the start date to one day ahead
                        n += 1
                        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
                        start_date += datetime.timedelta(days=1)
                        start = start_date.strftime("%Y-%m-%d")


        elif stock_type == "JPMorgan":
            first_date = await sync_to_async(JPMStock.objects.first)()
            last_date = await sync_to_async(JPMStock.objects.last)()
            # If date entered is before start or after last date, allow javascript to pick up error
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() < first_date.date:
                await self.send(json.dumps({'first_date': first_date.date.isoformat()}))
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() > last_date.date:
                await self.send(json.dumps({'last_date': last_date.date.isoformat()}))
            jpm_stocks = await sync_to_async(list)(
                JPMStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )
            if jpm_stocks[0].date.isoformat() == start:
                if data.get('take_profit') or data.get("stop_loss"):
                    # Sends the user's balance to change in the page dynamically
                    await self.send(json.dumps({"date": jpm_stocks[0].date.isoformat(), "close": jpm_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                else:
                    await self.send(json.dumps({"date": jpm_stocks[0].date.isoformat(), "close": jpm_stocks[0].close}))
                await sleep(1)
            else:
                n = 1
                # Loop is needed as some days are not available in the dataset
                while n < len(jpm_stocks):
                    if jpm_stocks[0].date.isoformat() == start:
                        if data.get('take_profit') or data.get("stop_loss"):
                            # Sends the user's balance to change in the page dynamically
                            await self.send(json.dumps({"date": jpm_stocks[0].date.isoformat(), "close": jpm_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                        else:
                            await self.send(json.dumps({"date": jpm_stocks[0].date.isoformat(), "close": jpm_stocks[0].close}))
                        await sleep(1)
                        break
                    else:
                        # Changes the start date to one day ahead
                        n += 1
                        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
                        start_date += datetime.timedelta(days=1)
                        start = start_date.strftime("%Y-%m-%d")


        elif stock_type == "BankofAmerica":
            first_date = await sync_to_async(BACStock.objects.first)()
            last_date = await sync_to_async(BACStock.objects.last)()
            # If date entered is before start or after last date, allow javascript to pick up error
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() < first_date.date:
                await self.send(json.dumps({'first_date': first_date.date.isoformat()}))
            if datetime.datetime.strptime(start, '%Y-%m-%d').date() > last_date.date:
                await self.send(json.dumps({'last_date': last_date.date.isoformat()}))
            bac_stocks = await sync_to_async(list)(
                BACStock.objects.filter(date__gte=make_aware(datetime.datetime.strptime(start, '%Y-%m-%d')))
            )
            if bac_stocks[0].date.isoformat() == start:
                if data.get('take_profit') or data.get("stop_loss"):
                    # Sends the user's balance to change in the page dynamically
                    await self.send(json.dumps({"date": bac_stocks[0].date.isoformat(), "close": bac_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                else:
                    await self.send(json.dumps({"date": bac_stocks[0].date.isoformat(), "close": bac_stocks[0].close}))
                await sleep(1)
            else:
                n = 1
                # Loop is needed as some days are not available in the dataset
                while n < len(bac_stocks):
                    if bac_stocks[0].date.isoformat() == start:
                        if data.get('take_profit') or data.get("stop_loss"):
                            # Sends the user's balance to change in the page dynamically
                            await self.send(json.dumps({"date": bac_stocks[0].date.isoformat(), "close": bac_stocks[0].close, "money_in_account": user_profile.money_in_account}))
                        else:
                            await self.send(json.dumps({"date": bac_stocks[0].date.isoformat(), "close": bac_stocks[0].close}))
                        await sleep(1)
                        break
                    else:
                        # Changes the start date to one day ahead
                        n += 1
                        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
                        start_date += datetime.timedelta(days=1)
                        start = start_date.strftime("%Y-%m-%d")

    def disconnect(self, event):
        print('websocket disconnected...', event)
        self.end = True
        raise StopConsumer()