# blog/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/slug/<slug:slug>/', BlogPostViewSet.as_view({'get': 'retrieve'}), name='blogpost-detail-by-slug'),
]
