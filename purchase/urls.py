# purchase/urls.py
from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('ordenes-compra/', views.listar_ordenes_compra, name='ordenes_compra'),
    path('orden-compra/<int:orden_id>/', views.detalle_orden_compra, name='detalle_orden_compra'),
    path('orden-compra/crear/', views.crear_orden_compra, name='crear_orden_compra'),
    path('orden-compra/<int:orden_id>/aprobar/', views.aprobar_orden, name='aprobar_orden'),
    path('orden-compra/<int:orden_id>/rechazar/', views.rechazar_orden, name='rechazar_orden'),
]