from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Esta es la ruta para la página de inicio
    path('index/', views.index, name='website_index'),  # Cambia la ruta para index
    path('coche/<int:coche_id>/', views.coche_detalle, name='website_coche_detalle'),
]
