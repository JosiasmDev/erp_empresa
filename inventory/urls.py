from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.gestionar_stock, name='gestionar_stock'),
    path('editar/<int:stock_id>/', views.editar_stock, name='editar_stock'),
    path('verificar-stock/<int:orden_fabricacion_id>/', views.verificar_stock, name='verificar_stock'),
]