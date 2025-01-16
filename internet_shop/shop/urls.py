from django.urls import path
from shop import views 

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'), 
    path('contacts/', views.contacts, name='contacts'),
]
