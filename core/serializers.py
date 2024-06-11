from typing import Any, Dict
from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer

from core.models import Customer, ProductManager


class UserCreateSerializer(BaseUserCreateSerializer):
    username = serializers.CharField(read_only=True)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'full_name', 'user_role']

    def create(self, validated_data):
        user = super().create(validated_data)
        user_role = validated_data.get('user_role')
        
        profile_class = None
        if user_role == settings.K_MANAGER_USER_ROLE:
            profile_class = ProductManager
        elif user_role == settings.K_CUSTOMER_USER_ROLE:
            profile_class = Customer
        # Create the associated user profile based on role
        if profile_class is not None:
            profile_class.objects.create(user=user)
        
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
    
    
class ProductManagerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    id = serializers.IntegerField(source='user.id', read_only=True)
    full_name = serializers.IntegerField(source='user.full_name', read_only=True)
    email = serializers.IntegerField(source='user.email', read_only=True)
    phone = serializers.IntegerField(source='user.phone', read_only=True)
    user_role = serializers.IntegerField(source='user.user_role', read_only=True)
    joined = serializers.IntegerField(source='user.date_joined', read_only=True)
    
    class Meta:
        model = ProductManager
        fields = ['id', 'full_name', 'email', 'phone', 'profile_image', 'user_role', 'joined', 'user']
    
    
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    id = serializers.IntegerField(source='user.id', read_only=True)
    full_name = serializers.IntegerField(source='user.full_name', read_only=True)
    email = serializers.IntegerField(source='user.email', read_only=True)
    phone = serializers.IntegerField(source='user.phone', read_only=True)
    user_role = serializers.IntegerField(source='user.user_role', read_only=True)
    joined = serializers.IntegerField(source='user.date_joined', read_only=True)
    
    class Meta:
        model = ProductManager
        fields = ['id', 'full_name', 'email', 'phone', 'user_role', 'joined', 'user']
