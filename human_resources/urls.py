from django.urls import path
from . import views

urlpatterns = [
    path('', views.empleados, name='hr_empleados'),
    path('crear/', views.crear_empleado, name='hr_crear_empleado'),
]