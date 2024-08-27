from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WholesalerCompany, WholesalerBranch


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
