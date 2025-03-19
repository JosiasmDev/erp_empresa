from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('api/actualizar-tareas/', views.actualizar_tareas, name='actualizar_tareas'),
] 