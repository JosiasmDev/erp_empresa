from django.urls import path
from . import views

urlpatterns = [
    path('', views.compras, name='purchase_compras'),
    path('purchase_form/<int:coche_id>/', views.purchase_form, name='purchase_form'),
    path('process_payment/<int:compra_id>/', views.process_payment, name='purchase_process_payment'),
]