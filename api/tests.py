
from django.contrib.auth.models import User
# from django.test import TestCase
# from rest_framework.test import APIClient
from django.urls import reverse
# from v1.web.views import LoginViewSet, GetOtpViewSet
# from datetime import timedelta
# from django.utils import timezone
# from api.models import *

# class LoginViewSetTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username=7018716110, email='test@example.com', password='testpass')

#     def test_successful_login(self):
#         url = reverse('login-list') 
#         data = {
#             'identity': 7018716110,
#             'password': 'testpass'
#         }
#         response = self.client.post(url, data=data, format='json')
#         self.assertEqual(response.data['status'], True)
#         self.assertEqual(response.data['message'], 'login success')

#     def test_invalid_password(self):
#         url = reverse('login-list')  
#         data = {
#             'identity': 7018716110,
#             'password': 'wrongpass'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.data['status'], False)
#         self.assertEqual(response.data['message'], 'password not valid')
       

#     def test_user_not_found(self):
#         url = reverse('login-list')  
#         data = {
#             'identity': 'nonexistent',
#             'password': 'testpass'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.data['status'], False)
#         self.assertEqual(response.data['message'], 'user not found')
    



from django.test import TestCase
from rest_framework.test import APIClient

class GetOtpViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_with_valid_data(self):
        url = reverse('get_otp-list')
        data = {
            'phone': '1234567890',
            'email': 'test@example.com',
            'full_name': 'John Doe',
            'password': 'password123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['status'],True)
        self.assertEqual(response.data['message'], 'Otp sent')
        print('Otp sent')


    def test_create_with_existing_phone(self):
        url = reverse('get_otp-list')
        data = {
            'phone': 'existing_phone_number',
            'email': 'test@example.com',
            'full_name': 'John Doe',
            'password': 'password123',
        }
        User.objects.create(username='existing_phone_number')
        response = self.client.post(url, data)
        self.assertEqual(response.data['status'],False)
        self.assertEqual(response.data['message'], 'Phone number already exists')
        print( 'Phone number already exists')

    def test_create_with_invalid_data(self):
        url = reverse('get_otp-list')
        data = {
            'phone': '1234567890',
            'email': 'invalid_email',
            'full_name': '',
            'password': '',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['status'],False)
        self.assertEqual(response.data['message'], 'Otp Sending Failed')
        print('Otp Sending Failed')
   




def test_missing_required_fields(self):
        url = reverse('get_otp-list')
        data = {
            'email': 'test@example.com',
            'full_name': 'John Doe',
            'password': 'password123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['status'],False)
        print(4)
        

def test_invalid_phone_number(self):
        url = reverse('get_otp-list')
        data = {
            'phone': 'invalid_phone_number',
            'email': 'test@example.com',
            'full_name': 'John Doe',
            'password': 'password123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['status'],False)
        print(5)
    

def test_incorrect_otp(self):
        url = reverse('get_otp-list')
        data = {
            'id': 1,  
            'otp': 'incorrect_otp',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['status'],False)
        print(6)
       

def test_successful_user_registration(self):
        url = reverse('get_otp-list')
        data = {
            'phone': '1234567890',
            'email': 'test@example.com',
            'full_name': 'John Doe',
            'password': 'password123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['status'],True)
        self.assertEqual(response.data['message'], 'Otp sent')
        self.assertIn('id', response.data)
        print(7)

        

