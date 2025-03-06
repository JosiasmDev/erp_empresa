from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='website_index'),
    path('crear/', views.crear_pagina, name='website_crear_pagina'),
]