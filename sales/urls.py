from django.urls import path
from . import views

urlpatterns = [
    path('', views.pedidos, name='sales_pedidos'),
]