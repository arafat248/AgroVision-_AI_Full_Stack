from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users.serializers import UserSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    role = serializers.ChoiceField(
        choices=User.Roles.choices,
        default=User.Roles.FARMER
    )
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone', 'password', 'role', 'organization')
    def validate_email(self, value):
        normalized_email = value.lower()
        if User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return normalized_email
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone=validated_data.get('phone'),
            role=validated_data.get('role', User.Roles.FARMER),
            organization=validated_data.get('organization')
        )
        return user
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Token Pair serializer that adds user details in response data
    """
    def validate(self, attrs):
        # The parent validate returns access and refresh tokens
        data = super().validate(attrs)
        
        # Add custom fields to responses
        user_serializer = UserSerializer(self.user)
        data['user'] = user_serializer.data
        return data
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value
    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("New password cannot be the same as the old password.")
        return data
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate_email(self, value):
        normalized_email = value.lower()
        if not User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError("No user is registered with this email.")
        return normalized_email