from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_register, name='login_register'),  # Asegúrate de que el nombre sea 'login_register'
    path('logout/', views.logout_view, name='logout'),
    path('crear-empleado/', views.create_employee, name='create_employee'),
]