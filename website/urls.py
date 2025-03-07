from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='website_index'),
    path('coche/<int:coche_id>/', views.coche_detalle, name='website_coche_detalle'),
]