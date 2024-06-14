from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('markdownx/', include('markdownx.urls')),
    path('profile/', include('core.urls')),
    path('order/', include('order.urls')),
    path('product/', include('product.urls')),
    path('blog/', include('blog.urls')),
]
