from datetime import timezone
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from core.models import User
from product.models import Product


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
    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    promo_code = models.ForeignKey(PromoCode, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=settings.K_STATUS_PENDING)

    def __str__(self):
        if self.user:
            return f"Order {self.id} by {self.user.full_name} ({self.user.email})"
        else:
            return f"Order {self.id} by a deleted user"
    
    def get_discounted_total(self):
        if self.promo_code and self.promo_code.is_valid() and self.total >= self.promo_code.min_order_amount:
            discount_amount = self.total * (self.promo_code.discount / 100)
            return self.total - discount_amount
        return self.total
    
    def update_total(self):
        self.total = sum(item.quantity * item.price for item in self.items.all())
        self.save()
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    
@receiver(pre_save, sender=OrderItem)
def set_order_item_price(sender, instance, **kwargs):
    if instance.product:
        instance.price = instance.product.price


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    instance.order.update_total()

