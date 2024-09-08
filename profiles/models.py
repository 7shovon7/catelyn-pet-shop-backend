from django.db import models
from django.conf import settings

from core.models import User


# Wholesaler
class WholesalerCompany(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.title
    
    
class WholesalerBranch(models.Model):
    wholesaler = models.ForeignKey(WholesalerCompany, on_delete=models.CASCADE, related_name='branches')
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.get_branch_title()
    
    def get_branch_title(self):
        return f"{self.wholesaler.title} - {self.title}"
    
    
class WholesalerAddress(models.Model):
    branch = models.ForeignKey(WholesalerBranch, on_delete=models.CASCADE, related_name='addresses')
    is_primary = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    area = models.CharField(max_length=255, blank=True, null=True)
    # TODO: have to add certain list of choices for district and division
    district = models.CharField(max_length=255, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.address
    
    
class WholesalerContact(models.Model):
    branch = models.ForeignKey(WholesalerBranch, on_delete=models.CASCADE, related_name='contacts')
    is_primary = models.BooleanField(default=True)
    person_name = models.CharField(max_length=255)
    post = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.person_name
    
    
# Customer
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    
    def __str__(self) -> str:
        return self.user.full_name if self.user else "Deleted User"
    
    
class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    is_primary = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    area = models.CharField(max_length=255, blank=True, null=True)
    # TODO: have to add certain list of choices for district and division
    district = models.CharField(max_length=255, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.customer.user.full_name} - {self.address}"
    

class CustomerContact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    is_primary = models.BooleanField(default=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.customer.user.full_name} - {self.phone} | {self.email}"
