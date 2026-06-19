from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from users.serializers import UserSerializer
from .serializers import (RegisterSerializer, CustomTokenObtainPairSerializer,
    ChangePasswordSerializer, ResetPasswordSerializer
)
User = get_user_model()
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    @extend_schema(
        summary="Register a new user",
        description="Creates a new user profile. Roles can be Farmer, Agriculture Officer, or Admin.",
        responses={
            201: UserSerializer,
            400: OpenApiResponse(description="Invalid request payload or email already exists.")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens automatically for instant login on registration
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        
        return Response({
            'message': 'User registered successfully.',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': user_data
        }, status=status.HTTP_201_CREATED)
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    @extend_schema(
        summary="Obtain JWT Tokens (Login)",
        description="Authenticates credentials and returns access & refresh tokens along with user details.",
        responses={
            200: OpenApiResponse(description="Login successful. Returns tokens and user details."),
            401: OpenApiResponse(description="Invalid credentials.")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    @extend_schema(
        summary="Logout User",
        description="Blacklists the provided refresh token, invalidating the session.",
        request={'application/json': {'type': 'object', 'properties': {'refresh': {'type': 'string'}}, 'required': ['refresh']}},
        responses={
            200: OpenApiResponse(description="Successfully logged out."),
            400: OpenApiResponse(description="Token is invalid or expired.")
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    @extend_schema(
        summary="Change Password",
        description="Updates the password of the authenticated user.",
        responses={
            200: OpenApiResponse(description="Password changed successfully."),
            400: OpenApiResponse(description="Validation error with passwords.")
        }
    )
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
    @extend_schema(exclude=True)
    def patch(self, request, *args, **kwargs):
        return Response({"detail": "Method PATCH not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ResetPasswordSerializer
    @extend_schema(
        summary="Reset Password Request",
        description="Initiates password reset flow. Sends a mock reset token.",
        responses={
            200: OpenApiResponse(description="Password reset email simulated successfully."),
            400: OpenApiResponse(description="Email not found.")
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        # Mocking email trigger
        import uuid
        reset_token = uuid.uuid4().hex
        
        # In actual production, this would dispatch an email async
        return Response({
            "message": f"Password reset instructions sent to {email}.",
            "reset_token": reset_token,
            "note": "This is a mock endpoint in dev. Use this token to reset your password."
        }, status=status.HTTP_200_OK)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self):
        return self.request.user
    @extend_schema(
        summary="Retrieve Current User Profile",
        description="Returns details of the currently authenticated user.",
        responses={200: UserSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    @extend_schema(
        summary="Update Current User Profile",
        description="Updates profile details of the currently authenticated user.",
        responses={200: UserSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    @extend_schema(
        summary="Patch Current User Profile",
        description="Partially updates profile details of the currently authenticated user.",
        responses={200: UserSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
