from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from core.utils import change_profile_image_filename


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [ (r, r) for r in settings.K_CUSTOM_USER_ROLES ]

    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=100)
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True, default=settings.K_CUSTOMER_USER_ROLE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'user_role']

    objects = UserManager()
    
    
# class ProductManager(models.Model):
#     phone = models.CharField(max_length=30, null=True, blank=True)
#     profile_image = models.ImageField(upload_to=change_profile_image_filename, null=True, blank=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='manager')
    
#     def __str__(self) -> str:
#         return self.user.full_name
    
    
# class Customer(models.Model):
#     phone = models.CharField(max_length=30, null=True, blank=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer')
    
#     def __str__(self) -> str:
#         return self.user.full_name
    
    
# class Address(models.Model):
#     local_adress = models.CharField(max_length=255)
#     post_code = models.CharField(max_length=4)
#     district = models.CharField(max_length=50)
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
