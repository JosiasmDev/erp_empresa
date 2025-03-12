# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_register, name='login'),  # Usaremos 'login'
    path('logout/', views.logout_view, name='logout'),
    path('crear-empleado/', views.create_employee, name='create_employee'),
]
