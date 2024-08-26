# product/serializers.py
from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'description', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.CharField(source="category.title")
    categories = CategorySerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'discounted_price', 'available_stock', 'total_sold', 'size', 'size_unit', 'categories', 'image', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']
