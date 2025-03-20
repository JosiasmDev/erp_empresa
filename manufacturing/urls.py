# manufacturing/urls.py
from django.urls import path
from . import views

app_name = 'manufacturing'

urlpatterns = [
    path('', views.lista_ordenes, name='lista_ordenes'),
    path('produccion/', views.manufacturing_produccion, name='produccion'),
    path('orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('orden/crear/', views.crear_orden, name='crear_orden'),
    path('orden/<int:orden_id>/editar/', views.editar_orden, name='editar_orden'),
    path('orden/<int:orden_id>/eliminar/', views.eliminar_orden, name='eliminar_orden'),
]