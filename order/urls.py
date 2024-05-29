from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromoCodeViewSet, OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'promocodes', PromoCodeViewSet)
router.register(r'items', OrderItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
