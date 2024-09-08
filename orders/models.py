from django.conf import settings
from django.db import models
from django.utils import timezone

from profiles.models import Customer, CustomerAddress, CustomerContact
from shipments.models import ShipmentProduct


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 20.00 for 20% discount
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to


class Order(models.Model):
    STATUS_CHOICES = [(c, c) for c in settings.K_ORDER_STATUS_LIST]
    # TODO: have to add static customer and address string here to save these 2 permanently and the proper signals
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    title = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(CustomerAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=settings.K_STATUS_PENDING)
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    def calculate_total(self):
        return sum(item.calculate_total_order_item_price() for item in self.items.all())
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.title:
            self.title = f"{self.customer.user.full_name} - {self.created_at}"
        if self.pk:
            self.total_price = self.calculate_total()
            if self.promo_code and self.promo_code.is_valid():
                self.discounted_price = self.total_price * (1 - self.promo_code.discount / 100)
            else:
                self.discounted_price = None
        super().save(*args, **kwargs)
    

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
        self.shipment_product.product.available_stock -= quantity_to_be_updated
        self.shipment_product.product.save()
        self.shipment_product.stock -= quantity_to_be_updated
        self.shipment_product.save()
        # Update complete order total
        self.order.save()
        super().save(*args, **kwargs)
        
    def calculate_total_order_item_price(self):
        return self.selling_price_per_unit * self.quantity
