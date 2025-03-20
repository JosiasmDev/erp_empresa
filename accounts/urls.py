# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'  # Añadir el app_name para el namespace

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-employee/', views.create_employee, name='create_employee'),
    path('perfil/', views.perfil, name='perfil'),
    path('register/', views.register, name='register'),  # Nueva URL para registro
]
