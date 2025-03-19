# erp_empresa/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('website/', include('website.urls')),
    path('', RedirectView.as_view(url='/ecommerce/', permanent=True), name='index'),
    path('accounts/', include('accounts.urls')),
    path('ecommerce/', include('ecommerce.urls')),
    path('crm/', include('crm.urls')),
    path('sales/', include('sales.urls')),
    path('purchase/', RedirectView.as_view(url='/purchase/ordenes-compra/', permanent=True)),
    path('purchase/', include('purchase.urls')),
    path('manufacturing/', include('manufacturing.urls')),
    path('inventory/', include('inventory.urls')),
    path('accounting/', include('accounting.urls')),
    path('human_resources/', include('human_resources.urls')),
    path('marketing_automation/', include('marketing_automation.urls')),
]