from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register('', views.UserViewSet, basename='user_view_set')

urlpatterns = router.urls
