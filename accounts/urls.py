# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'  # Añadir el app_name para el namespace

urlpatterns = [
    path('login/', views.login_register, name='login'),  # Usaremos 'login'
    path('logout/', views.logout_view, name='logout'),
    path('crear-empleado/', views.create_employee, name='create_employee'),
]
