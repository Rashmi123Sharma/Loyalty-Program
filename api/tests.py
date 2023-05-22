from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.viewsets import ViewSet

class LoginTestCase(APITestCase):
    def test_login_success(self):
        url = reverse('v1/web/login')  # Replace 'login' with the actual name or URL pattern of your login view
        data = {
            'identity': 'test1@gmail.com',
            'password': 'password123',
        }
        response = self.client.post(url, data=data, format="json")
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['status'], True)


   
    # def login_fail(self):
    #     _data={
    #     'identity':'test1@gmail.com',
    #     'password':'password123',
    #       }
    #     _response=self.client.post('v1/web/login',data=_data,format="json")
    #     _data=_response.json()
    #     print(_data)
    #     self.assertEqual(_data['status'],False)


