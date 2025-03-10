from django.urls import path
from . import views

urlpatterns = [
    path('', views.pedidos, name='sales_pedidos'),
    path('crear/', views.crear_pedido, name='sales_crear_pedido'),
    path('agregar_item/<int:pedido_id>/', views.agregar_item, name='sales_agregar_item'),
]