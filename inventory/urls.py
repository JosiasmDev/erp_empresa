from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock, name='inventory_stock'),
    path('crear/', views.crear_movimiento, name='inventory_crear_movimiento'),
]