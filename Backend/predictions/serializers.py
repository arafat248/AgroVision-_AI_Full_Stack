from rest_framework import serializers
from .models import PredictionHistory

class PredictionInputSerializer(serializers.Serializer):
    nitrogen = serializers.FloatField(
        required=True,
        min_value=0.0,
        max_value=300.0,
        help_text="Nitrogen (N) content in soil (mg/kg)"
    )
    phosphorus = serializers.FloatField(
        required=True,
        min_value=0.0,
        max_value=300.0,
        help_text="Phosphorus (P) content in soil (mg/kg)"
    )
    potassium = serializers.FloatField(
        required=True,
        min_value=0.0,
        max_value=300.0,
        help_text="Potassium (K) content in soil (mg/kg)"
    )
    temperature = serializers.FloatField(
        required=True,
        min_value=-10.0,
        max_value=60.0,
        help_text="Temperature in degrees Celsius"
    )
    humidity = serializers.FloatField(
        required=True,
        min_value=0.0,
        max_value=100.0,
        help_text="Relative humidity percentage"
    )
    ph = serializers.FloatField(
        required=True,
        min_value=0.0,
        max_value=14.0,
        help_text="pH value of the soil (0 to 14)"
    )
    rainfall = serializers.FloatField(
        required=True,
        min_value=0.0,
        max_value=1000.0,
        help_text="Rainfall in millimeters (mm)"
    )
class PredictionHistorySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    class Meta:
        model = PredictionHistory
        fields = (
            'id',
            'user',
            'user_email',
            'user_full_name',
            'predicted_crop',
            'confidence_score',
            'risk_level',
            'nitrogen',
            'phosphorus',
            'potassium',
            'temperature',
            'humidity',
            'ph',
            'rainfall',
            'created_at'
        )
        read_only_fields = ('id', 'user', 'predicted_crop', 'confidence_score', 'risk_level', 'created_at')