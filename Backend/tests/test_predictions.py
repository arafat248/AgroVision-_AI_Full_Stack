from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from predictions.models import PredictionHistory

User = get_user_model()
class PredictionTests(APITestCase):
    def setUp(self):
        self.predict_url = reverse('predict')
        self.history_list_url = reverse('prediction_history-list')
        # Create users
        self.farmer = User.objects.create_user(
            email='farmer@test.com', password='password123', full_name='Farmer Joe', role='Farmer'
        )
        self.farmer2 = User.objects.create_user(
            email='farmer2@test.com', password='password123', full_name='Farmer Pete', role='Farmer'
        )
        self.officer = User.objects.create_user(
            email='officer@test.com', password='password123', full_name='Officer Smith', role='Agriculture Officer'
        )
        # Create sample prediction history records
        self.p1 = PredictionHistory.objects.create(
            user=self.farmer, predicted_crop='Rice', confidence_score=95.0, risk_level='Low',
            nitrogen=90, phosphorus=42, potassium=43, temperature=20.8, humidity=82.0, ph=6.5, rainfall=202.9
        )
        self.p2 = PredictionHistory.objects.create(
            user=self.farmer2, predicted_crop='Maize', confidence_score=75.0, risk_level='Medium',
            nitrogen=70, phosphorus=35, potassium=30, temperature=24.5, humidity=65.0, ph=6.0, rainfall=95.5
        )
    def test_predict_success_farmer(self):
        self.client.force_authenticate(user=self.farmer)
        data = {
            'nitrogen': 80.0,
            'phosphorus': 40.0,
            'potassium': 40.0,
            'temperature': 25.0,
            'humidity': 80.0,
            'ph': 6.5,
            'rainfall': 200.0
        }
        response = self.client.post(self.predict_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('predicted_crop', response.data)
        self.assertIn('confidence_score', response.data)
        self.assertIn('risk_level', response.data)
        self.assertIn('alternative_crops', response.data)
        
        # Verify database record saved
        history_count = PredictionHistory.objects.filter(user=self.farmer).count()
        self.assertEqual(history_count, 2) # 1 setup + 1 new
    def test_predict_forbidden_officer(self):
        self.client.force_authenticate(user=self.officer)
        data = {
            'nitrogen': 80.0, 'phosphorus': 40.0, 'potassium': 40.0,
            'temperature': 25.0, 'humidity': 80.0, 'ph': 6.5, 'rainfall': 200.0
        }
        response = self.client.post(self.predict_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_predict_validation_error(self):
        self.client.force_authenticate(user=self.farmer)
        data = {
            'nitrogen': -10.0, # invalid
            'phosphorus': 40.0,
            'potassium': 40.0,
            'temperature': 25.0,
            'humidity': 120.0, # invalid
            'ph': 15.0, # invalid
            'rainfall': 200.0
        }
        response = self.client.post(self.predict_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nitrogen', response.data['details'])
        self.assertIn('humidity', response.data['details'])
        self.assertIn('ph', response.data['details'])
    def test_history_list_scope_farmer(self):
        # Farmer should only see their own records
        self.client.force_authenticate(user=self.farmer)
        response = self.client.get(self.history_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], str(self.p1.id))
    def test_history_list_scope_officer(self):
        # Officer should see all records
        self.client.force_authenticate(user=self.officer)
        response = self.client.get(self.history_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    def test_history_detail_farmer(self):
        self.client.force_authenticate(user=self.farmer)
        detail_url = reverse('prediction_history-detail', args=[self.p1.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['predicted_crop'], 'Rice')
    def test_history_detail_farmer_unauthorized(self):
        # Farmer Joe trying to access Farmer Pete's record
        self.client.force_authenticate(user=self.farmer)
        detail_url = reverse('prediction_history-detail', args=[self.p2.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_history_filtering_and_search(self):
        self.client.force_authenticate(user=self.officer)
        
        # Filter by crop
        response = self.client.get(self.history_list_url, {'predicted_crop': 'Rice'})
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['predicted_crop'], 'Rice')
        # Filter by risk level
        response = self.client.get(self.history_list_url, {'risk_level': 'Medium'})
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['predicted_crop'], 'Maize')