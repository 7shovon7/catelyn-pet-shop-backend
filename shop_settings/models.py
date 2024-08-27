from django.db import models
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