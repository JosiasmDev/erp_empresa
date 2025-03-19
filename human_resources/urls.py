from django.urls import path
from . import views

app_name = 'human_resources'

urlpatterns = [
    path('', views.empleados, name='empleados'),
    path('empleado/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleado/<int:empleado_id>/editar/', views.editar_empleado, name='editar_empleado'),
    path('empleado/<int:empleado_id>/eliminar/', views.eliminar_empleado, name='eliminar_empleado'),
]