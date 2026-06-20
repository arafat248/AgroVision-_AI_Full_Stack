from django.urls import path
from .views import DashboardView, ChartsView, FeatureImportanceView, DataQualityView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='analytics_dashboard'),
    path('charts/', ChartsView.as_view(), name='analytics_charts'),
    path('feature-importance/', FeatureImportanceView.as_view(), name='analytics_feature_importance'),
    path('data-quality/', DataQualityView.as_view(), name='analytics_data_quality'),
]