from django.contrib import admin
from .models import Order, OrderItem
from .forms import OrderAdminForm


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = ['customer', 'address', 'total_price']
    # search_fields = ['customer__']
    
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'order', 'selling_price_per_unit', 'quantity']
