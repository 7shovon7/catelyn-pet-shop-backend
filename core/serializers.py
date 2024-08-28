from typing import Any, Dict
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer

from .models import User

# from core.models import Customer, ProductManager


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'full_name', 'user_role']

    def create(self, validated_data):
        user = super().create(validated_data)
        user_role = validated_data.get('user_role')
        
        # profile_class = None
        # if user_role == settings.K_MANAGER_USER_ROLE:
        #     profile_class = ProductManager
        # elif user_role == settings.K_CUSTOMER_USER_ROLE:
        #     profile_class = Customer
        # # Create the associated user profile based on role
        # if profile_class is not None:
        #     profile_class.objects.create(user=user)
        
        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'full_name', 'user_role']
        

class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['full_name'] = user.full_name
        token['user_role'] = user.user_role
        return token
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        
        data['user'] = {
            "id": self.user.id,
            "email": self.user.email,
            "full_name": self.user.full_name,
            "user_role": self.user.user_role
        }
        return data
    
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_reset_code()

        # Prepare email context
        context = {
            'reset_code': user.reset_code,
            'site_name': 'Catelyn Pet Shop',
            'full_name': user.full_name,
        }

        # Render the HTML template
        html_content = render_to_string('emails/password_reset.html', context)
        text_content = strip_tags(html_content)

        # Send email
        email = EmailMultiAlternatives(
            subject="Password Reset on Catelyn Pet Shop",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        
class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if not user or not user.validate_reset_code(data['reset_code']):
            raise serializers.ValidationError("Invalid reset code or email.")
        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.clear_reset_code()
        user.save()
