from django.urls import path
from . import views

urlpatterns = [
    path('', views.compras, name='purchase_compras'),
    path('crear/', views.crear_compra, name='purchase_crear_compra'),
]