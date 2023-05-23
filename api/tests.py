
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from v1.web.views import LoginViewSet

class LoginViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_successful_login(self):
        url = reverse('login-list') 
        data = {
            'identity': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.data['status'], True)
        self.assertEqual(response.data['message'], 'login success')
        self.assertIsNotNone(response.data['token'])
        self.assertIsNotNone(response.data['user_data'])

    def test_invalid_password(self):
        url = reverse('login-list')  
        data = {
            'identity': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['message'], 'password not valid')
        self.assertNotIn('token', response.data)
        self.assertNotIn('user_data', response.data)

    def test_user_not_found(self):
        url = reverse('login-list')  
        data = {
            'identity': 'nonexistent',
            'password': 'testpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['message'], 'user not found')
        self.assertNotIn('token', response.data)
        self.assertNotIn('user_data', response.data)
