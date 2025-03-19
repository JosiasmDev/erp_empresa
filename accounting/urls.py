from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ingresos/', views.ingresos, name='ingresos'),
    path('gastos/', views.gastos, name='gastos'),
    path('balance/', views.balance, name='balance'),
    path('facturas/', views.facturas, name='facturas'),
    path('crear/', views.crear_factura, name='crear_factura'),
]