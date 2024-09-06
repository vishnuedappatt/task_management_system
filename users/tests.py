from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from users.models import CustomUser

class UserAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.user_list_url = reverse('user list')
        self.admin_user = CustomUser.objects.create_user(
            name='Admin User', email='admin@example.com', password='adminpass', is_admin=True
        )
        self.normal_user = CustomUser.objects.create_user(
            name='Normal User', email='user@example.com', password='userpass'
        )

    def test_signup(self):
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['email'], data['email'])


    def test_login(self):
        data = {
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        self.client.post(self.signup_url, {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword"
    }, format='json')

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  

    def test_user_list_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)  
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_list_as_non_admin(self):
        self.client.force_authenticate(user=self.normal_user) 
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 