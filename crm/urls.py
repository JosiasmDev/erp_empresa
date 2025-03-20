from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.clientes, name='clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
]