# purchase/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.compras, name='purchase_compras'),
    path('crear/', views.crear_compra, name='purchase_crear_compra'),
    path('editar/<int:compra_id>/', views.editar_compra, name='purchase_editar_compra'),
    path('eliminar/<int:compra_id>/', views.eliminar_compra, name='purchase_eliminar_compra'),
    path('process-payment/<int:compra_id>/', views.process_payment, name='purchase_process_payment'),
]