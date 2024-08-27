# product/admin.py

from django.contrib import admin
from .models import Product, Review

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_at', 'updated_at')
#     search_fields = ('title',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'discounted_price', 'available_stock', 'created_at', 'updated_at')
    search_fields = ('title',)
    filter_horizontal = ('categories',)
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'comment', 'created_at', 'updated_at')
    search_fields = ('user__username', 'product__title')
    list_filter = ('rating', 'created_at')
