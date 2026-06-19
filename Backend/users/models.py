import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        FARMER = 'Farmer', _('Farmer')
        OFFICER = 'Agriculture Officer', _('Agriculture Officer')
        ADMIN = 'Admin', _('Admin')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    full_name = models.CharField(_('full name'), max_length=255)
    phone = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    role = models.CharField(
        _('role'),
        max_length=50,
        choices=Roles.choices,
        default=Roles.FARMER
    )
    organization = models.CharField(_('organization'), max_length=255, blank=True, null=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.email} ({self.role})"