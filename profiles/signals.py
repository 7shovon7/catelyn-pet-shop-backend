from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import WholesalerCompany, WholesalerBranch, Customer

@receiver(post_save, sender=WholesalerCompany)
def apply_new_company_name(sender, instance, **kwargs):
    branches = instance.branches.all()
    for branch in branches:
        branch_title = branch.get_branch_title()
        # Update all shipments associated with this branch
        branch.shipments.update(wholesaler_title=branch_title)
        
        
@receiver(post_save, sender=WholesalerBranch)
def update_shipments_on_branch_update(sender, instance, **kwargs):
    branch_title = instance.get_branch_title()
    instance.shipments.update(wholesaler_title=branch_title)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_profile(sender, instance, created, **kwargs):
    if created and instance.user_role == settings.K_CUSTOMER_USER_ROLE:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_customer_profile(sender, instance, **kwargs):
    if instance.user_role == settings.K_CUSTOMER_USER_ROLE:
        if hasattr(instance, 'customer'):
            instance.customer.save()
        else:
            Customer.objects.create(user=instance)
