from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name='crm_clientes'),
    path('crear/', views.crear_cliente, name='crm_crear_cliente'),
]