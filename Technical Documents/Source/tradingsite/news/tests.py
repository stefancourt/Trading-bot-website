from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import UserProfile
from trade.models import AAPLStock, MSFTStock

# Testing the View
class NewsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='user_1', password='password')
        self.user_profile = UserProfile.objects.create(user=self.user, money_in_account=1000.00)
        AAPLStock.objects.create(date="2014-05-02", open=210, close=220, high=230, low=200)
        AAPLStock.objects.create(date="2014-05-03", open=210, close=220, high=230, low=200)
        MSFTStock.objects.create(date="2014-05-02", open=210, close=220, high=230, low=200)
        MSFTStock.objects.create(date="2014-05-03", open=210, close=220, high=230, low=200)

    def test_news_view_authenticated(self):
        """Test news view for authenticated user"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)

    def test_news_view_unauthenticated(self):
        """Test news view for unauthenticated user"""
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/') 