from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from core.models import User
from core.utils import optimize_image_in_upload_model
from shop_settings.models import Category, CustomField


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = MarkdownxField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_stock = models.PositiveIntegerField(default=0)
    total_sold = models.PositiveIntegerField(default=0)
    size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    size_unit = models.CharField(max_length=20, choices=settings.K_SIZE_UNITS, blank=True, null=True)
    # category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = optimize_image_in_upload_model(self.image, desired_height=600)
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        # Check if any shipment_item has non-zero stock
        if self.shipment_items.filter(stock__gt=0).exists():
            raise ValidationError("Can't delete this product as it's associated shipment items with non-zero stock.")
        super().delete(*args, **kwargs)
    
    def formatted_markdown(self):
        return markdownify(self.description)
    
    
class CustomFieldData(models.Model):
    product = models.ForeignKey(Product, related_name='custom_fields', on_delete=models.CASCADE)
    field = models.ForeignKey(CustomField, related_name='fields', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f"{self.field.name}: {self.value}"
    
    class Meta:
        unique_together = ['product', 'field']


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
