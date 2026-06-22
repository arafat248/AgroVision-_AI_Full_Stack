from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
User = get_user_model()
class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('auth_login')
        self.profile_url = reverse('auth_profile')
        self.change_password_url = reverse('auth_change_password')
        self.reset_password_url = reverse('auth_reset_password')
        
        # Create a default user
        self.user_data = {
            'email': 'farmer@agro.com',
            'password': 'StrongPassword123!',
            'full_name': 'John Farmer',
            'phone': '1234567890',
            'role': 'Farmer',
            'organization': 'Green Farms Ltd'
        }
        self.user = User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            full_name=self.user_data['full_name'],
            phone=self.user_data['phone'],
            role=self.user_data['role'],
            organization=self.user_data['organization']
        )
    def test_user_registration(self):
        url = self.register_url
        data = {
            'email': 'newfarmer@agro.com',
            'password': 'SecurePassword456!',
            'full_name': 'Jane Farmer',
            'phone': '0987654321',
            'role': 'Farmer',
            'organization': 'Organics Corp'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['email'], 'newfarmer@agro.com')
    def test_user_registration_duplicate_email(self):
        url = self.register_url
        data = {
            'email': 'farmer@agro.com',  # existing
            'password': 'SecurePassword456!',
            'full_name': 'Jane Farmer',
            'phone': '0987654321',
            'role': 'Farmer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['details'])
    def test_user_login(self):
        url = self.login_url
        data = {
            'email': 'farmer@agro.com',
            'password': 'StrongPassword123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], 'farmer@agro.com')
    def test_user_login_invalid_credentials(self):
        url = self.login_url
        data = {
            'email': 'farmer@agro.com',
            'password': 'WrongPassword!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_retrieve_user_profile(self):
        # Authenticate client
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'farmer@agro.com')
        self.assertEqual(response.data['role'], 'Farmer')
    def test_update_user_profile(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'full_name': 'John Farmer Edited',
            'phone': '5555555'
        }
        response = self.client.patch(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'John Farmer Edited')
        self.assertEqual(response.data['phone'], '5555555')
    def test_change_password(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'StrongPassword123!',
            'new_password': 'NewStrongPassword321!'
        }
        response = self.client.put(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check login works with new password
        self.client.force_authenticate(user=None)
        login_response = self.client.post(self.login_url, {
            'email': 'farmer@agro.com',
            'password': 'NewStrongPassword321!'
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
    def test_reset_password_request(self):
        data = {'email': 'farmer@agro.com'}
        response = self.client.post(self.reset_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('reset_token', response.data)
