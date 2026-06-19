from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, ChangePasswordView,
    ResetPasswordView, UserProfileView
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='auth_reset_password'),
    path('profile/', UserProfileView.as_view(), name='auth_profile'),
]