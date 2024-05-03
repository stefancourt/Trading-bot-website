from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from main.models import UserProfile
from django.urls import reverse 
from .forms import DateForm, AmountForm, AITypeForm, TypeForm, PlaceTradeForm
from .models import AAPLStock, MSFTStock, StockType, PFEStock, JNJStock, JPMStock, BACStock, AMZNStock, NVDAStock, TSLAStock, METAStock, XOMStock, PEPStock
from .views import trade_view
from datetime import date
import json

# Testing the Forms
class DateFormTest(TestCase):
    def test_date_form_widget_attrs(self):
        form = DateForm()
        self.assertIn('class="form-date"', str(form['start']))

class AmountFormTest(TestCase):
    def test_amount_form_widget_attrs(self):
        form = AmountForm()
        self.assertIn('class="form-amount"', str(form['amount']))

class AITypeFormTest(TestCase):
    def test_ai_type_form_widget_attrs(self):
        form = AITypeForm()
        self.assertIn('class="radio-input"', str(form['order_type']))

class TypeFormTest(TestCase):
    def test_type_form_widget_attrs(self):
        form = TypeForm()
        self.assertIn('class="form-type"', str(form['stock_type']))

class PlaceTradeFormTest(TestCase):
    def test_place_trade_form_widget_attrs(self):
        form = PlaceTradeForm()
        self.assertIn('class="form-control"', str(form['take_profit']))
        self.assertIn('class="form-control"', str(form['stop_loss']))
        self.assertIn('class="radio-input"', str(form['order_type']))

# Testing the models
class AAPLStockModelTest(TestCase):
    def test_aapl_stock_ordering(self):
        AAPLStock.objects.create(date=date(2023, 1, 1), open=100, close=110, high=115, low=95)
        AAPLStock.objects.create(date=date(2023, 1, 2), open=110, close=120, high=125, low=105)
        aapl_stocks = AAPLStock.objects.all()
        self.assertEqual(aapl_stocks[0].date, date(2023, 1, 1))

class MSFTStockModelTest(TestCase):
    def test_msft_stock_ordering(self):
        MSFTStock.objects.create(date=date(2023, 1, 1), open=200, close=210, high=215, low=195)
        MSFTStock.objects.create(date=date(2023, 1, 2), open=210, close=220, high=225, low=205)
        msft_stocks = MSFTStock.objects.all()
        self.assertEqual(msft_stocks[0].date, date(2023, 1, 1))

class StockTypeModelTest(TestCase):
    def test_stock_type_choices(self):
        stock_type = StockType.objects.create(stock_type='Apple')
        self.assertEqual(stock_type.get_stock_type_display(), 'Apple')

# Test the View
class TradeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='user_1', password='password')
        self.user_profile = UserProfile.objects.create(user=self.user, money_in_account=1000.00)
        self.apple_stock = AAPLStock.objects.create(date=date(2014, 1, 1), open=110, close=120, high=125, low=105)
        self.microsoft_stock = MSFTStock.objects.create(date=date(2014, 1, 1), open=110, close=120, high=125, low=105)
        self.apple_stock = AAPLStock.objects.create(date=date(2014, 1, 2), open=120, close=130, high=135, low=115)
        self.microsoft_stock = MSFTStock.objects.create(date=date(2014, 1, 2), open=120, close=130, high=135, low=115)
        self.jnj_stock = JNJStock.objects.create(date=date(2014, 1, 1), open=110, close=120, high=125, low=105)
        self.jnj_stock = JNJStock.objects.create(date=date(2014, 1, 2), open=110, close=120, high=125, low=105)
        self.pfe_stock = PFEStock.objects.create(date=date(2014, 1, 1), open=120, close=130, high=135, low=115)
        self.pfe_stock = PFEStock.objects.create(date=date(2014, 1, 2), open=120, close=130, high=135, low=115)
        self.jpm_stock = JPMStock.objects.create(date=date(2014, 1, 1), open=110, close=120, high=125, low=105)
        self.jpm_stock = JPMStock.objects.create(date=date(2014, 1, 2), open=110, close=120, high=125, low=105)
        self.bac_stock = BACStock.objects.create(date=date(2014, 1, 1), open=120, close=130, high=135, low=115)
        self.bac_stock = BACStock.objects.create(date=date(2014, 1, 2), open=120, close=130, high=135, low=115)
        self.amazon_stock = AMZNStock.objects.create(date=date(2014, 1, 1), open=110, close=120, high=125, low=105)
        self.amazon_stock = AMZNStock.objects.create(date=date(2014, 1, 2), open=110, close=120, high=125, low=105)
        self.nvidia_stock = NVDAStock.objects.create(date=date(2014, 1, 1), open=120, close=130, high=135, low=115)
        self.nvidia_stock = NVDAStock.objects.create(date=date(2014, 1, 2), open=120, close=130, high=135, low=115)
        self.tesla_stock = TSLAStock.objects.create(date=date(2014, 1, 1), open=110, close=120, high=125, low=105)
        self.tesla_stock = TSLAStock.objects.create(date=date(2014, 1, 2), open=110, close=120, high=125, low=105)
        self.meta_stock = METAStock.objects.create(date=date(2014, 1, 1), open=120, close=130, high=135, low=115)
        self.meta_stock = METAStock.objects.create(date=date(2014, 1, 2), open=120, close=130, high=135, low=115)
        self.xom_stock = XOMStock.objects.create(date=date(2014, 1, 1), open=110, close=120, high=125, low=105)
        self.xom_stock = XOMStock.objects.create(date=date(2014, 1, 2), open=110, close=120, high=125, low=105)
        self.pep_stock = PEPStock.objects.create(date=date(2014, 1, 1), open=120, close=130, high=135, low=115)
        self.pep_stock = PEPStock.objects.create(date=date(2014, 1, 2), open=120, close=130, high=135, low=115)

    def test_trade_view_authenticated_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('trade'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trade/trade.html')
        self.assertIsInstance(response.context['place_trade_form'], PlaceTradeForm)
        self.assertIsInstance(response.context['date_form'], DateForm)
        self.assertIsInstance(response.context['stock_type_form'], TypeForm)
        self.assertEqual(float(response.context['money_in_account']), 1000.00)
        self.assertEqual(float(response.context['apple']), 130.00)
        self.assertEqual(float(response.context['apple_change']), 10.00)
        self.assertEqual(float(response.context['microsoft']), 130.00)
        self.assertEqual(float(response.context['microsoft_change']), 10.00)

    def test_trade_view_authenticated_post(self):
        request = self.factory.post('/trade/', data={'amount': 100, 'stop_loss': 80, 'take_profit': 110, 'order_type': 'buy'})
        request.user = self.user
        response = trade_view(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['stop_loss'], str(80))
        self.assertEqual(data['take_profit'], str(110))
        self.assertEqual(data['order_type'], 'buy')

    def test_trade_view_unauthenticated(self):
        response = self.client.get(reverse('trade'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')