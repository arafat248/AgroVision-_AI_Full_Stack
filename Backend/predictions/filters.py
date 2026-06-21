import django_filters
from .models import PredictionHistory

class PredictionHistoryFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    predicted_crop = django_filters.CharFilter(field_name='predicted_crop', lookup_expr='iexact')
    risk_level = django_filters.CharFilter(field_name='risk_level', lookup_expr='iexact')
    farmer_email = django_filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    class Meta:
        model = PredictionHistory
        fields = ['predicted_crop', 'risk_level', 'farmer_email']