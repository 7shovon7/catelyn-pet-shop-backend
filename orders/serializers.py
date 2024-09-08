from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem, PromoCode
from profiles.models import Customer, CustomerAddress
from shipments.models import ShipmentProduct

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['id', 'code', 'discount', 'active', 'valid_from', 'valid_to', 'min_order_amount']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'shipment_product', 'title', 'selling_price_per_unit', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'title', 'address', 'total_price', 'promo_code', 'discounted_price', 'created_at', 'status', 'items']
        read_only_fields = ['total_price', 'discounted_price']

    def get_items(self, obj):
        if isinstance(obj, Order):
            return OrderItemSerializer(obj.items.all(), many=True).data
        return []

    def validate_items(self, items_data):
        for item in items_data:
            shipment_product_id = item.get('shipment_product')
            quantity = item.get('quantity', 1)
            try:
                shipment_product = ShipmentProduct.objects.get(id=shipment_product_id)
                if shipment_product.stock < quantity:
                    raise serializers.ValidationError(f"Not enough stock for product {shipment_product.product_name}. Available: {shipment_product.stock}")
            except ShipmentProduct.DoesNotExist:
                raise serializers.ValidationError(f"ShipmentProduct with id {shipment_product_id} does not exist.")
        return items_data

    @transaction.atomic
    def create(self, validated_data):
        items_data = self.context['request'].data.get('items', [])
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            shipment_product_id = item_data.get('shipment_product')
            quantity = item_data.get('quantity', 1)
            if shipment_product_id:
                shipment_product = ShipmentProduct.objects.get(id=shipment_product_id)
                OrderItem.objects.create(order=order, shipment_product=shipment_product, quantity=quantity)
                shipment_product.stock -= quantity
                shipment_product.save()
        
        order.save()
        return order
