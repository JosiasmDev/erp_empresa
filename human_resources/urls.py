from django.urls import path
from . import views

urlpatterns = [
    path('', views.empleados, name='hr_empleados'),
]