from rest_framework import serializers

from product.models import Product
from .models import PromoCode, Order, OrderItem

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        # read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    # total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'total', 'items']
        # read_only_fields = ['user']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product'].id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )
        order.update_total()
        # request = self.context.get('request', None)
        # if request is not None:
        #     validated_data['user'] = request.user
        # return super().create(validated_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                product = Product.objects.get(id=item_data['product'].id)
                OrderItem.objects.create(
                    order=instance, 
                    product=product, 
                    quantity=item_data['quantity'], 
                    price=product.price  # Set the price from the product
                )
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        instance.updated_total()
        return instance
