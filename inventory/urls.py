from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', RedirectView.as_view(url='/inventory/stock/', permanent=True), name='inventory_index'),
    path('stock/', views.gestionar_stock, name='inventory_stock'),
    path('movimiento/crear/', views.crear_movimiento, name='inventory_crear_movimiento'),
    path('stock/editar/', views.editar_stock, name='inventory_editar_stock'),
    path('verificar-stock/<int:orden_fabricacion_id>/', views.verificar_stock, name='verificar_stock'),
    path('api/proveedores/', views.get_proveedores, name='get_proveedores'),
]