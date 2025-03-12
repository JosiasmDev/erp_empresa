# website/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('coche/<int:coche_id>/', views.coche_detalle, name='coche_detalle'),
    path('contacto/', views.contacto, name='contacto'),
    path('home/', views.home, name='home'),
]