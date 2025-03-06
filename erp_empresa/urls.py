from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('website/', include('website.urls')),
    path('crm/', include('crm.urls')),
    path('ecommerce/', include('ecommerce.urls')),
    path('sales/', include('sales.urls')),
    path('hr/', include('human_resources.urls')),
    path('manufacturing/', include('manufacturing.urls')),
    path('marketing/', include('marketing_automation.urls')),
    path('inventory/', include('inventory.urls')),
    path('accounting/', include('accounting.urls')),
    path('purchase/', include('purchase.urls')),
    path('', views.home, name='home'),
]