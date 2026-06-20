from rest_framework import permissions

class IsFarmer(permissions.BasePermission):
    """
    Custom permission to only allow Farmers or Admins.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'Farmer' or request.user.role == 'Admin'
class IsAgricultureOfficer(permissions.BasePermission):
    """
    Custom permission to only allow Agriculture Officers or Admins.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'Agriculture Officer' or request.user.role == 'Admin'
class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow Admins.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'Admin'
class IsFarmerOrOfficer(permissions.BasePermission):
    """
    Custom permission to allow Farmers, Officers, or Admins.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['Farmer', 'Agriculture Officer', 'Admin']