from django.contrib import admin
from .models import Shipment, ShipmentProduct


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'wholesaler_title', 'price_value', 'discounted_price_value']
    search_fields = ['wholesaler_title']
    # list_filter = ['category']

@admin.register(ShipmentProduct)
class ShipmentProductAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'product_name', 'box', 'quantity_per_box', 'price_per_box', 'stock')
    readonly_fields = ('product_name', 'stock')  # Always read-only fields
    
    def get_readonly_fields(self, request, obj=None):
        # If the object exists (i.e., it's being edited), make certain fields read-only
        if obj:
            return self.readonly_fields + ('box', 'quantity_per_box', 'price_per_box')
        return self.readonly_fields

    # def has_change_permission(self, request, obj=None):
    #     # Disallow any changes to existing objects; only allow creation
    #     if obj:
    #         return False
    #     return super().has_change_permission(request, obj)

    # def has_delete_permission(self, request, obj=None):
    #     # Disallow deletion of ShipmentProduct objects
    #     return True

    # def has_add_permission(self, request):
    #     # Allow adding new ShipmentProduct objects
    #     return True
