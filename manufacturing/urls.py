# manufacturing/urls.py
from django.urls import path
from . import views

app_name = 'manufacturing'

urlpatterns = [
    path('', views.ordenes_fabricacion, name='ordenes_fabricacion'),
    path('orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('crear/', views.crear_orden, name='crear_orden'),
]