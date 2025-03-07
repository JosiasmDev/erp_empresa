from django.urls import path
from . import views

urlpatterns = [
    path('purchase/<int:coche_id>/', views.purchase_form, name='purchase_form'),
    path('payment/<int:compra_id>/', views.process_payment, name='process_payment'),
]