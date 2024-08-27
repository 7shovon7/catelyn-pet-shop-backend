from django.db import models

from profiles.models import Customer, CustomerAddress, CustomerContact
from shipments.models import ShipmentProduct


class Order(models.Model):
    # TODO: have to add static customer and address string here to save these 2 permanently and the proper signals
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    address = models.ForeignKey(CustomerAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    def calculate_total(self):
        return sum(item.calculate_total_order_item_price() for item in self.items.all())
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.title:
            self.title = f"{self.customer.user.full_name} - {self.created_at}"
        if self.pk:
            self.total_price = self.calculate_total()
        return super().save(*args, **kwargs)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    shipment_product = models.ForeignKey(ShipmentProduct, on_delete=models.PROTECT, related_name='order_items')
    title = models.CharField(max_length=255, blank=True, null=True)
    selling_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    quantity = models.IntegerField(default=1, blank=True)
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.selling_price_per_unit:
                # Create selling_price_per_unit
                self.selling_price_per_unit = self.shipment_product.product.discounted_price if self.shipment_product.product.discounted_price else self.shipment_product.product.price
                
            quantity_to_be_updated = self.quantity
        else:
            original_item = OrderItem.objects.get(pk=self.pk)
            quantity_to_be_updated = self.quantity - original_item.quantity
        
        # Update stock in Product and ShipmentProduct
        self.shipment_product.product.stock -= quantity_to_be_updated
        self.shipment_product.product.save()
        self.shipment_product.stock -= quantity_to_be_updated
        self.shipment_product.save()
        # Update complete order total
        self.order.save()
        super().save(*args, **kwargs)
        
    def calculate_total_order_item_price(self):
        return self.selling_price_per_unit * self.quantity
