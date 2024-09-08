from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, PromoCodeViewSet

router = DefaultRouter()
router.register(r'order-items', OrderItemViewSet, basename='orderitem')
router.register(r'promo-codes', PromoCodeViewSet)
router.register(r'list', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
