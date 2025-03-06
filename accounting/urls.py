from django.urls import path
from . import views

urlpatterns = [
    path('', views.facturas, name='accounting_facturas'),
    path('crear/', views.crear_factura, name='accounting_crear_factura'),
]