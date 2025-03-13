from django.urls import path
from . import views

app_name = 'marketing_automation'

urlpatterns = [
    path('', views.campanas, name='campanas'),
    path('crear/', views.crear_campana, name='crear_campana'),
    path('lista_coches/', views.lista_coches, name='lista_coches'),
    path('editar_coche/<int:coche_id>/', views.editar_coche, name='editar_coche'),
    path('editar_todos_coches/', views.editar_todos_coches, name='editar_todos_coches'),
]