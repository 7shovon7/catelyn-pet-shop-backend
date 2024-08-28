from django.urls import path
# from rest_framework.routers import SimpleRouter
from .views import PasswordResetView, PasswordResetConfirmView


# router = SimpleRouter()
# router.register('', views.UserViewSet, basename='user_view_set')

urlpatterns = [
    path('users/reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('users/reset_password_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
