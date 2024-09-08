from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem, PromoCode
from shipments.models import ShipmentProduct

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'selling_price_per_unit', 'title']
        read_only_fields = ['id', 'selling_price_per_unit', 'title']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'title', 'address', 'total_price', 'promo_code', 'discounted_price', 'created_at', 'status', 'items']
        read_only_fields = ['id', 'customer', 'total_price', 'discounted_price', 'created_at', 'status']

    def validate_items(self, items_data):
        for item in items_data:
            product_id = item.get('product')
            quantity = item.get('quantity', 1)
            try:
                shipment_product = ShipmentProduct.objects.filter(
                    product_id=product_id, 
                    stock__gt=0
                ).order_by('shipment__created_at').first()
                
                if not shipment_product:
                    raise serializers.ValidationError(f"Product with id {product_id} is out of stock.")
                if shipment_product.stock < quantity:
                    raise serializers.ValidationError(f"Not enough stock for product {shipment_product.product.title}. Available: {shipment_product.stock}")
            except ShipmentProduct.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} does not exist.")
        return items_data

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product_id = item_data.pop('product')
            quantity = item_data.get('quantity', 1)
            
            shipment_product = ShipmentProduct.objects.filter(
                product_id=product_id, 
                stock__gt=0
            ).order_by('shipment__created_at').first()
            
            OrderItem.objects.create(
                order=order, 
                shipment_product=shipment_product,
                quantity=quantity,
                selling_price_per_unit=shipment_product.product.discounted_price or shipment_product.product.price,
                title=shipment_product.product.title
            )
        
        order.save()  # This will trigger the save method in the Order model to calculate the total
        return order

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['id', 'code', 'discount', 'active', 'valid_from', 'valid_to', 'min_order_amount']
