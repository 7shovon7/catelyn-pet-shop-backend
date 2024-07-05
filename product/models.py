# product/models.py

from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from core.models import User
from core.utils import optimize_image_in_upload_model


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='product/categories/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = optimize_image_in_upload_model(self.image, desired_height=300)
        super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = MarkdownxField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = optimize_image_in_upload_model(self.image, desired_height=600)
        super().save(*args, **kwargs)
    
    def formatted_markdown(self):
        return markdownify(self.description)


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
