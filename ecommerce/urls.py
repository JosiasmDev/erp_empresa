from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name='ecommerce_tienda'),
    path('crear/', views.crear_coche, name='ecommerce_crear_coche'),
]