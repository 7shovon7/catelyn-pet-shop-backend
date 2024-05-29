# order/views.py
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import PromoCode, Order, OrderItem
from .serializers import PromoCodeSerializer, OrderSerializer, OrderItemSerializer

class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.validated_data.get('order')
        product = serializer.validated_data.get('product')
        quantity = serializer.validated_data.get('quantity')

        # Check if the order belongs to the authenticated user
        if order.user != self.request.user:
            raise serializers.ValidationError("You are not allowed to add items to this order.")

        # Check if an OrderItem for this product already exists in this order
        existing_order_item = OrderItem.objects.filter(order=order, product=product).first()

        if existing_order_item:
            existing_order_item.quantity += quantity
            existing_order_item.save()
        else:
            serializer.save()

    def perform_update(self, serializer):
        order = serializer.validated_data.get('order')
        if order.user != self.request.user:
            raise serializers.ValidationError("You are not allowed to update items in this order.")
        serializer.save()
