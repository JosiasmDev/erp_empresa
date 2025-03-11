from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),  # Esto maneja la ruta principal
    path('accounts/', include('accounts.urls')),
    path('ecommerce/', include('ecommerce.urls')),
    path('crm/', include('crm.urls')),
    path('sales/', include('sales.urls')),
    path('purchase/', include('purchase.urls')),
    path('manufacturing/', include('manufacturing.urls')),
    path('inventory/', include('inventory.urls')),
    path('accounting/', include('accounting.urls')),
    path('human_resources/', include('human_resources.urls')),
    path('marketing_automation/', include('marketing_automation.urls')),
]
