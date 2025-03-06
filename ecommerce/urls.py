from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name='ecommerce_tienda'),
]