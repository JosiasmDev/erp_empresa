from django.urls import path
from . import views

urlpatterns = [
    path('', views.campanas, name='marketing_campanas'),
]