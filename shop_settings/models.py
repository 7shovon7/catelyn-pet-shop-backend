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
        
        
class CustomField(models.Model):
    name = models.CharField(max_length=100, unique=True)
    key = models.CharField(max_length=100, editable=False, null=True)
    is_required = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.key:
            base_key = self.name.lower().replace(' ', '-')
            key = base_key
            counter = 1
            while CustomField.objects.filter(key=key).exists():
                key = f"{base_key}-{counter}"
                counter += 1
                
            self.key = key
        
        return super().save(*args, **kwargs)
