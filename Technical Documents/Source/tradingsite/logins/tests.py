from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from .views import register_view, login_view, logout_view
from django.contrib.auth import login, logout
from django.urls import reverse
from .forms import RegisterUserForm, CustomAuthenticationForm
from main.models import UserProfile
from django.contrib.auth import authenticate

# Testing Forms
class RegisterUserFormTestCase(TestCase):
    def test_valid_form(self):
        """Test RegisterUserForm with valid data"""
        form_data = {
            'username': 'testuser',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }
        form = RegisterUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Test RegisterUserForm with invalid data"""
        form_data = {
            'username': 'testuser',
            'password1': 'TestPassword123',
            'password2': 'DifferentPassword',  # Invalid password confirmation
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())

class CustomAuthenticationFormTestCase(TestCase):
    def test_valid_login(self):
        """Test CustomAuthenticationForm with valid credentials"""
        # Create a test user
        User.objects.create_user(username='testuser', password='TestPassword123')
        
        form_data = {
            'username': 'testuser',
            'password': 'TestPassword123',
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login(self):
        """Test CustomAuthenticationForm with invalid credentials"""
        form_data = {
            'username': 'testuser',
            'password': 'InvalidPassword',
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())

# Testing Views

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_register_view_get(self):
        """Test register view with GET request"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegisterUserForm)

    def test_register_view_post_valid_form(self):
        """Test register view with POST request and valid form data"""
        form_data = {'username': 'testuser', 'password1': 'TestPassword123', 'password2': 'TestPassword123'}
        request = self.factory.post('/register/', data=form_data)
        response = register_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_post_invalid_form(self):
        """Test register view with POST request and invalid form data"""
        form_data = {'username': 'testuser', 'password1': 'TestPassword123', 'password2': 'DifferentPassword'}
        request = self.factory.post('/register/', data=form_data)
        response = register_view(request)
        self.assertEqual(response.status_code, 200)

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='TestPassword123')

    def test_login_view_get(self):
        """Test login view with GET request"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

    def test_login_view_post_valid_credentials(self):
        """Test login view with POST request and valid credentials"""
        form_data = {'username': 'testuser', 'password': 'TestPassword123'}
        response = self.client.post(reverse('login'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirects to stats page
        self.assertEqual(response.url, '/stats')  # Redirects to stats page on successful login
        # Ensure user is authenticated
        self.assertTrue(authenticate(username='testuser', password='TestPassword123'))

    def test_login_view_post_invalid_credentials(self):
        """Test login view with POST request and invalid credentials"""
        form_data = {'username': 'testuser', 'password': 'InvalidPassword'}
        request = self.factory.post('/login/', data=form_data)
        response = login_view(request)
        self.assertEqual(response.status_code, 200)  # Form is not valid, should stay on login page

class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='TestPassword123')

    def test_logout_view_post(self):
        """Test logout view with POST request"""
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertEqual(response.url, '/')  # Redirects to login page after logout

    # Add more test cases to cover other scenarios, if applicable.

