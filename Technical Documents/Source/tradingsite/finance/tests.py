from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from main.models import UserProfile
from finance.views import finance_view
from django.urls import reverse
from finance.forms import ManageForm
from django.http import JsonResponse
import json
# Testing the Forms
class ManageFormTest(TestCase):
    def test_manage_form_valid_data(self):
        form_data = {
            'rent': 300,
            'bills': 100,
            'food': 80,
            'invest': 100,
            'savings': 100,
            'luxury': 200,
            'choices': 'Bar'
        }
        form = ManageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manage_form_invalid_data(self):
        form_data = {
            'rent': 'not_an_integer',
            'bills': 300,
            'food': 200,
            'invest': 50,
            'savings': 100,
            'luxury': 200,
            'choices': 'Pie'
        }
        form = ManageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rent', form.errors)

    def test_manage_form_widget_attrs(self):
        form = ManageForm()
        self.assertIn('class="form-control"', str(form['rent']))
        self.assertIn('class="form-select third"', str(form['choices']))

# Testing the View
class FinanceViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='user_1', password='password')
        self.user_profile = UserProfile.objects.create(user=self.user, money_in_account=1000.00)

    def test_finance_view_authenticated_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('finance'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'finance/finance.html')
        self.assertIsInstance(response.context['manage_form'], ManageForm)

    def test_finance_view_authenticated_post(self):
        request = self.factory.post('/finance/', data={'rent': 200, 'bills': 100, 'food': 300, 'invest': 100, 'savings': 50, 'luxury': 150, 'choices': 'Pie'})
        request.user = self.user
        response = finance_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        data = json.loads(response.content)
        self.assertEqual(data['choices'], 'Pie')
        self.assertEqual(data['rent'], 200)

    def test_finance_view_unauthenticated(self):
        response = self.client.get(reverse('finance'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

