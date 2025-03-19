# manufacturing/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.manufacturing_produccion, name='manufacturing_produccion'),  # Cambiado de views.produccion a views.manufacturing_produccion
    path('crear/', views.crear_orden, name='manufacturing_crear_orden'),
]