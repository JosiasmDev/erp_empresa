from django.urls import path
from . import views

urlpatterns = [
    path('', views.campanas, name='marketing_campanas'),
    path('crear/', views.crear_campana, name='marketing_crear_campana'),
]