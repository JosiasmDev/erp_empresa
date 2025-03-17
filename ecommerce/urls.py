# ecommerce/urls.py
from django.urls import path
from . import views

app_name = 'ecommerce'  # Añadido para definir el namespace

urlpatterns = [
    path('', views.ecommerce_dashboard, name='ecommerce_dashboard'),
    path('pasarela_pago/<int:coche_id>/', views.pasarela_pago, name='pasarela_pago'),
]