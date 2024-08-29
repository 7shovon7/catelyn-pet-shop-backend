from django.db import models

from product.models import Product
from profiles.models import WholesalerBranch


class Shipment(models.Model):
    wholesaler = models.ForeignKey(WholesalerBranch, on_delete=models.SET_NULL, related_name='shipments', null=True)
    wholesaler_title = models.CharField(max_length=255, editable=False, null=True)
    price_value = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.0)
    discounted_price_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.wholesaler_title} - {self.created_at}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.wholesaler_title = self.get_wholesaler_title()
        return super().save(*args, **kwargs)
            
    def get_wholesaler_title(self):
        if self.wholesaler:
            return f"{self.wholesaler.wholesaler.title} - {self.wholesaler.title}"
        return "Deleted wholesaler"
    

class ShipmentProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='shipment_items')
    # CAUTION 1: shipment_items is used in the following places:
    # 1. Product's delete method
    # 2. ProductAdmin's has_delete_permission method
    # CAUTION 2: product can't be null when creating, because it's needed for OrderItem
    product_name = models.CharField(max_length=255, blank=True, null=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='items')
    box = models.IntegerField(default=1)
    quantity_per_box = models.IntegerField(default=1)
    price_per_box = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock = models.IntegerField(default=1, editable=False)
    
    def __str__(self) -> str:
        return f"{self.shipment.wholesaler_title} - {self.product_name}"
    
    def save(self, *args, **kwargs):
        # Update stock only when created
        # User can't update stock here. If needed, they have to delete it and recreate
        if not self.pk:
            stock = self.calculate_this_shipment_product_stock()
            self.stock = stock
            
            if self.product:
                self.product.available_stock += stock
                self.product.save()

        # Keep track of the product name, in case the product is deleted
        if self.product:
            self.product_name = self.product.title
            
        # Update Shipment total
        new_price = self.calculate_this_shipment_product_price()
        self.shipment.price_value += new_price
        self.shipment.save()
        
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        self.product.available_stock -= self.calculate_this_shipment_product_stock()
        self.shipment.price_value -= self.calculate_this_shipment_product_price()
        return super().delete(*args, **kwargs)
        
    def calculate_this_shipment_product_stock(self):
        return self.box * self.quantity_per_box
        
    def calculate_this_shipment_product_price(self):
        return self.box * self.price_per_box
