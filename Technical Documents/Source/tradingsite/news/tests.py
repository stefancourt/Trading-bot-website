from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import UserProfile
from trade.models import AAPLStock, MSFTStock, JNJStock, PFEStock, JPMStock, BACStock,  AMZNStock, NVDAStock, TSLAStock, METAStock, XOMStock,  PEPStock, COSTStock, HDStock, ADBEStock, NKEStock

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
        JNJStock.objects.create(date="2014-05-02", open=110, close=120, high=125, low=105)
        JNJStock.objects.create(date="2014-05-03", open=110, close=120, high=125, low=105)
        PFEStock.objects.create(date="2014-05-02", open=120, close=130, high=135, low=115)
        PFEStock.objects.create(date="2014-05-03", open=120, close=130, high=135, low=115)
        JPMStock.objects.create(date="2014-05-02", open=110, close=120, high=125, low=105)
        JPMStock.objects.create(date="2014-05-03", open=110, close=120, high=125, low=105)
        BACStock.objects.create(date="2014-05-02", open=120, close=130, high=135, low=115)
        BACStock.objects.create(date="2014-05-03", open=120, close=130, high=135, low=115)
        AMZNStock.objects.create(date="2014-05-02", open=110, close=120, high=125, low=105)
        AMZNStock.objects.create(date="2014-05-03", open=110, close=120, high=125, low=105)
        NVDAStock.objects.create(date="2014-05-02", open=120, close=130, high=135, low=115)
        NVDAStock.objects.create(date="2014-05-03", open=120, close=130, high=135, low=115)
        TSLAStock.objects.create(date="2014-05-02", open=110, close=120, high=125, low=105)
        TSLAStock.objects.create(date="2014-05-03", open=110, close=120, high=125, low=105)
        METAStock.objects.create(date="2014-05-02", open=120, close=130, high=135, low=115)
        METAStock.objects.create(date="2014-05-03", open=120, close=130, high=135, low=115)
        XOMStock.objects.create(date="2014-05-02", open=110, close=120, high=125, low=105)
        XOMStock.objects.create(date="2014-05-03", open=110, close=120, high=125, low=105)
        PEPStock.objects.create(date="2014-05-02", open=120, close=130, high=135, low=115)
        PEPStock.objects.create(date="2014-05-03", open=120, close=130, high=135, low=115)
        COSTStock.objects.create(date="2014-05-02", open=110, close=120, high=125, low=105)
        COSTStock.objects.create(date="2014-05-03", open=110, close=120, high=125, low=105)
        HDStock.objects.create(date="2014-05-02", open=120, close=130, high=135, low=115)
        HDStock.objects.create(date="2014-05-03", open=120, close=130, high=135, low=115)
        ADBEStock.objects.create(date="2014-05-02", open=110, close=120, high=125, low=105)
        ADBEStock.objects.create(date="2014-05-03", open=110, close=120, high=125, low=105)
        NKEStock.objects.create(date="2014-05-02", open=120, close=130, high=135, low=115)
        NKEStock.objects.create(date="2014-05-03", open=120, close=130, high=135, low=115)

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