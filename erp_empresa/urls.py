# erp_empresa/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('website/', include('website.urls', namespace='website_ns')),
    path('', include('website.urls', namespace='website_root')),
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)