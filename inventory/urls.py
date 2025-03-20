from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', RedirectView.as_view(url='/inventory/stock/', permanent=True), name='inventory_index'),
    path('stock/', views.gestionar_stock, name='stock'),
    path('stock/editar/<int:stock_id>/', views.editar_stock, name='editar_stock'),
    path('movimiento/crear/', views.crear_movimiento, name='crear_movimiento'),
    path('verificar-stock/<int:orden_fabricacion_id>/', views.verificar_stock, name='verificar_stock'),
    path('get-proveedores/', views.get_proveedores, name='get_proveedores'),
]