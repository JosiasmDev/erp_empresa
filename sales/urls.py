from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.pedidos, name='pedidos'),
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('agregar_item/<int:pedido_id>/', views.agregar_item, name='agregar_item'),
]