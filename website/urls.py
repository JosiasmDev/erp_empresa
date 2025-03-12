from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Página de inicio
    path('contacto/', views.contacto, name='contacto'),
    path('coches/', views.coche_list, name='coche_list'),  # Nueva vista para listar coches
    path('coche/<int:coche_id>/', views.coche_detalle, name='coche_detalle'),  # Detalle de un coche
]