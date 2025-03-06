from django.urls import path
from . import views

urlpatterns = [
    path('', views.pedidos, name='sales_pedidos'),
    path('crear/', views.crear_pedido, name='sales_crear_pedido'),
    path('<int:pedido_id>/agregar-item/', views.agregar_item, name='sales_agregar_item'),
]