# website/urls.py
from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),  # Página de inicio
    path('contacto/', views.contacto, name='contacto'),
    path('coches/', views.coche_list, name='coche_list'),  # Nueva vista para listar coches
    path('coche/<int:coche_id>/', views.coche_detalle, name='coche_detalle'),  # Detalle de un coche
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
]