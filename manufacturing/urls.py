from django.urls import path
from . import views

urlpatterns = [
    path('', views.produccion, name='manufacturing_produccion'),
    path('crear/', views.crear_orden, name='manufacturing_crear_orden'),
]