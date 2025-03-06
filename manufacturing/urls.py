from django.urls import path
from . import views

urlpatterns = [
    path('', views.produccion, name='manufacturing_produccion'),
]