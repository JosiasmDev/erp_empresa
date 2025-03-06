from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name='ecommerce_tienda'),
    path('crear/', views.crear_producto, name='ecommerce_crear_producto'),
]