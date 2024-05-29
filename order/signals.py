# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Order, OrderProduct

# @receiver(post_save, sender=OrderProduct)
# @receiver(post_delete, sender=OrderProduct)
# def update_order_totals(sender, instance, **kwargs):
#     order = instance.order
#     order.calculate_final_total()
