from django.contrib import admin
from django.urls import path, include
from internet_shop.settings import DEBUG
from django.conf.urls.static import static
from internet_shop import settings 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    path('catalog/', include('tovari.urls', namespace='catalog')),
    path('user/', include('users.urls', namespace='users')),
    path('cart/', include('carts.urls', namespace='carts')),
    path('orders/', include('orders.urls', namespace='orders')),
] 

if DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)