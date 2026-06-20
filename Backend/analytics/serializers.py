from rest_framework import serializers

class DataQualityInputSerializer(serializers.Serializer):
    # All fields optional to allow computing completeness
    nitrogen = serializers.FloatField(required=False, allow_null=True)
    phosphorus = serializers.FloatField(required=False, allow_null=True)
    potassium = serializers.FloatField(required=False, allow_null=True)
    temperature = serializers.FloatField(required=False, allow_null=True)
    humidity = serializers.FloatField(required=False, allow_null=True)
    ph = serializers.FloatField(required=False, allow_null=True)
    rainfall = serializers.FloatField(required=False, allow_null=True)
