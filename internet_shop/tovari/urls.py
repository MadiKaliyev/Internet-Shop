from django.urls import path
from tovari.views import (
    ProductListAPIView, 
    ProductDetailAPIView, 
    generate_pdf, 
    catalog, 
    product
)

app_name = 'tovari'

urlpatterns = [
    # API маршруты
    path('api/products/', ProductListAPIView.as_view(), name='product_list'),
    path('api/products/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),

    # Маршруты каталога и товаров
    path('catalog/<slug:category_slug>/', catalog, name='catalog'),
    path('product/<slug:product_slug>/', product, name='product'),

    # Маршрут для генерации PDF
    path('generate-pdf/<slug:product_slug>/', generate_pdf, name='generate_pdf'),

    # Поиск (если используется)
    path('search/', catalog, name='search'),
    path('<slug:category_slug>/', catalog, name='index'),
]
