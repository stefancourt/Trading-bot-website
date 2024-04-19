from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from main.models import UserProfile, Trades
from django.urls import reverse
from trade.models import AAPLStock, MSFTStock
from trade.forms import DateForm, TypeForm, AmountForm, AITypeForm
from aitrade.views import aitrade_view
from datetime import date
import json

# Testing the View
class AITradeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile = UserProfile.objects.create(user=self.user, money_in_account=1000.00)
        self.apple_stock = AAPLStock.objects.create(date=date(2014, 1, 1), open=110, close=120, high=125, low=105)
        self.microsoft_stock = MSFTStock.objects.create(date=date(2014, 1, 1), open=110, close=120, high=125, low=105)
        self.apple_stock = AAPLStock.objects.create(date=date(2014, 1, 2), open=120, close=130, high=135, low=115)
        self.microsoft_stock = MSFTStock.objects.create(date=date(2014, 1, 2), open=120, close=130, high=135, low=115)
        self.trade = Trades.objects.create(user=self.user, pnl=50, total_pnl=100)

    def test_aitrade_view_authenticated_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('aitrade'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aitrade/ai-trade.html')
        self.assertIsInstance(response.context['date_form'], DateForm)
        self.assertIsInstance(response.context['ai_type_form'], AITypeForm)
        self.assertIsInstance(response.context['stock_type_form'], TypeForm)
        self.assertIsInstance(response.context['amount_form'], AmountForm)
        self.assertEqual(float(response.context['money_in_account']), 1000.00)
        self.assertEqual(float(response.context['apple']), 130.00)
        self.assertEqual(float(response.context['apple_change']), 10.00)
        self.assertEqual(float(response.context['microsoft']), 130.00)
        self.assertEqual(float(response.context['microsoft_change']), 10.00)
        self.assertEqual(response.context['trade_1'], 'Trade 1: 50.00')
        self.assertEqual(response.context['last_trade'], '100.00')

    def test_aitrade_view_authenticated_post(self):
        request = self.factory.post('/aitrade/')
        request.user = self.user
        response = aitrade_view(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['user_id'], self.user.id)

    def test_aitrade_view_unauthenticated_get(self):
        response = self.client.get(reverse('aitrade'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')