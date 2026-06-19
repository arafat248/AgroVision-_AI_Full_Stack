from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'full_name',
            'phone',
            'role',
            'organization',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'role', 'created_at', 'updated_at')