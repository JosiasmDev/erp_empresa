from django.urls import path
from . import views

urlpatterns = [
    path('', views.facturas, name='accounting_facturas'),
]