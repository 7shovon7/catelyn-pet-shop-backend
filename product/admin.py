# product/admin.py

from django.contrib import admin
from .models import CustomFieldData, Product, Review

class CustomFieldDataInline(admin.TabularInline):
    model = CustomFieldData
    extra = 1  # Number of extra empty forms to display

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'discounted_price', 'available_stock', 'custom_stock_out_signal', 'created_at', 'updated_at')
    search_fields = ('title',)
    filter_horizontal = ('categories',)
    inlines = [CustomFieldDataInline]
    
    def has_delete_permission(self, request, obj=None):
        if obj and obj.shipment_items.filter(stock__gt=0).exists():
            return False
        return super().has_delete_permission(request, obj)
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'comment', 'created_at', 'updated_at')
    search_fields = ('user__username', 'product__title')
    list_filter = ('rating', 'created_at')
