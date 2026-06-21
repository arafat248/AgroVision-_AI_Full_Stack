from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PredictView, PredictionHistoryViewSet

router = DefaultRouter()

router.register('history', PredictionHistoryViewSet, basename='prediction_history')

urlpatterns = [
    path('predict/', PredictView.as_view(), name='predict'),
    path('', include(router.urls)),
]
