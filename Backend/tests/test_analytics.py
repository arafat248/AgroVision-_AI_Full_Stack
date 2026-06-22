from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from predictions.models import PredictionHistory
User = get_user_model()
class AnalyticsTests(APITestCase):
    def setUp(self):
        self.dashboard_url = reverse('analytics_dashboard')
        self.charts_url = reverse('analytics_charts')
        self.importance_url = reverse('analytics_feature_importance')
        self.quality_url = reverse('analytics_data_quality')
        # Create users
        self.farmer = User.objects.create_user(
            email='farmer@test.com', password='password123', full_name='Farmer Joe', role='Farmer'
        )
        self.officer = User.objects.create_user(
            email='officer@test.com', password='password123', full_name='Officer Smith', role='Agriculture Officer'
        )
        # Create sample prediction history records
        PredictionHistory.objects.create(
            user=self.farmer, predicted_crop='Rice', confidence_score=90.0, risk_level='Low',
            nitrogen=90, phosphorus=42, potassium=43, temperature=20.8, humidity=82.0, ph=6.5, rainfall=202.9
        )
        PredictionHistory.objects.create(
            user=self.farmer, predicted_crop='Wheat', confidence_score=80.0, risk_level='Medium',
            nitrogen=70, phosphorus=35, potassium=30, temperature=24.5, humidity=65.0, ph=6.0, rainfall=95.5
        )
        PredictionHistory.objects.create(
            user=self.farmer, predicted_crop='Rice', confidence_score=95.0, risk_level='Low',
            nitrogen=95, phosphorus=45, potassium=45, temperature=22.0, humidity=85.0, ph=6.8, rainfall=210.0
        )
    def test_dashboard_metrics_officer_success(self):
        self.client.force_authenticate(user=self.officer)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_predictions'], 3)
        self.assertEqual(response.data['average_confidence'], 88.33)
        self.assertIn('accuracy_rate', response.data)
        self.assertEqual(response.data['most_predicted_crop'], 'Rice')
    def test_dashboard_metrics_farmer_forbidden(self):
        self.client.force_authenticate(user=self.farmer)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_charts_endpoint_success(self):
        self.client.force_authenticate(user=self.officer)
        response = self.client.get(self.charts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('monthly_prediction_trends', response.data)
        self.assertIn('crop_distribution', response.data)
        self.assertIn('confidence_distribution', response.data)
        self.assertIn('seasonal_recommendations', response.data)
    def test_feature_importance_success(self):
        self.client.force_authenticate(user=self.officer)
        response = self.client.get(self.importance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        self.assertIn('feature', response.data[0])
        self.assertIn('importance', response.data[0])
    def test_data_quality_endpoint_excellent(self):
        self.client.force_authenticate(user=self.officer)
        # Excellent dataset: no missing, no outliers
        data = {
            'nitrogen': 75.0,
            'phosphorus': 45.0,
            'potassium': 45.0,
            'temperature': 25.0,
            'humidity': 80.0,
            'ph': 6.5,
            'rainfall': 150.0
        }
        response = self.client.post(self.quality_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quality_status'], 'Excellent')
        self.assertEqual(response.data['completeness_score'], 100)
        self.assertEqual(response.data['reliability_score'], 100)
        self.assertEqual(response.data['outliers_detected'], 0)
    def test_data_quality_endpoint_with_missing_and_outliers(self):
        self.client.force_authenticate(user=self.officer)
        # Partial dataset with outliers:
        # missing: potassium (1 missing field)
        # outlier: temperature = 5.0 (limit is 10-48), ph = 13.0 (limit is 4.5-9) (2 outliers)
        data = {
            'nitrogen': 75.0,
            'phosphorus': 45.0,
            # 'potassium': missing
            'temperature': 5.0,
            'humidity': 80.0,
            'ph': 13.0,
            'rainfall': 150.0
        }
        response = self.client.post(self.quality_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Completeness: 6/7 present = 85%
        self.assertEqual(response.data['completeness_score'], 85)
        # Reliability: 100 - (1*15) - (2*10) = 100 - 15 - 20 = 65
        self.assertEqual(response.data['reliability_score'], 65)
        self.assertEqual(response.data['outliers_detected'], 2)
        self.assertEqual(response.data['quality_status'], 'Fair') # 65 falls in Fair (50 <= R < 75)
