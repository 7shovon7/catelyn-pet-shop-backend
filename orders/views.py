from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem, PromoCode
from .serializers import OrderSerializer, OrderItemSerializer, PromoCodeSerializer

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer__user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        order = self.get_object()
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            order.save()  # Recalculate total
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def apply_promo_code(self, request, pk=None):
        order = self.get_object()
        promo_code = request.data.get('promo_code')
        try:
            promo = PromoCode.objects.get(code=promo_code, active=True)
            if promo.is_valid() and order.total_price >= promo.min_order_amount:
                order.promo_code = promo
                order.save()
                return Response({"message": "Promo code applied successfully"})
            else:
                return Response({"error": "Invalid promo code or minimum order amount not met"}, status=status.HTTP_400_BAD_REQUEST)
        except PromoCode.DoesNotExist:
            return Response({"error": "Promo code not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__customer__user=self.request.user)

class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [IsAuthenticated]
