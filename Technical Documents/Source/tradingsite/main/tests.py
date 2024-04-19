from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Trades, UserProfile
from trade.models import StockType
from .forms import OverallTypeForm
import plotly.graph_objects as go
from .views import stats_view


# Testing the Models
class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.profile = UserProfile.objects.create(user=self.user, money_in_account=1000.00)

    def test_profile_creation(self):
        """Test UserProfile model creation"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.money_in_account, 1000.00)

class TradesModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.trade = Trades.objects.create(user=self.user, stock_name='Test Stock', pnl=100, total_pnl=100)

    def test_trade_creation(self):
        """Test Trades model creation"""
        self.assertEqual(self.trade.stock_name, 'Test Stock')
        self.assertEqual(self.trade.pnl, 100)
        self.assertEqual(self.trade.total_pnl, 100)

# Testing the Forms
class OverallTypeFormTestCase(TestCase):
    def test_form_widgets(self):
        """Test form widgets"""
        form = OverallTypeForm()
        self.assertIn('class="form-type"', str(form))
        self.assertIn('placeholder="Overall"', str(form))

    def test_form_field_required(self):
        """Test form field required attribute"""
        form = OverallTypeForm()
        self.assertFalse(form.fields['stock_type'].required)

    def test_form_save(self):
        """Test form save method"""
        data = {'stock_type': 'Apple'}
        form = OverallTypeForm(data)
        self.assertTrue(form.is_valid())
        stock_type_instance = form.save()
        self.assertIsInstance(stock_type_instance, StockType)
        self.assertEqual(stock_type_instance.stock_type, 'Apple')

# Testing the View
class StatsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, money_in_account=1000.00)
        self.trade = Trades.objects.create(user=self.user, stock_name='Test Stock', pnl=100, total_pnl=100)

    def test_authenticated_user(self):
        """Test stats view for authenticated user"""
        request = self.factory.get('/stats/')
        request.user = self.user
        response = stats_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Previous Trades Analysis', response.content)
        self.assertIn(b'Trade 1: 100.00', response.content)

    def test_unauthenticated_user(self):
        """Test stats view for unauthenticated user"""
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')