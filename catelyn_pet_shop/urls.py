from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('markdownx/', include('markdownx.urls')),
    # path('profile/', include('core.urls')),
    path('order/', include('order.urls')),
    path('product/', include('product.urls')),
    path('blog/', include('blog.urls')),
    path('shop_settings/', include('shop_settings.urls')),
    path('', include('core.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
