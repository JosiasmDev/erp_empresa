from django.contrib import admin
from django.urls import path, include
from website import views as website_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', website_views.index, name='website_index'),
    path('purchase/', include('purchase.urls')),
    path('manufacturing/', include('manufacturing.urls')),
    path('accounts/', include('accounts.urls')),
    path('ecommerce/', include('ecommerce.urls')),
    path('crm/', include('crm.urls')),
    path('sales/', include('sales.urls')),
    path('inventory/', include('inventory.urls')),
    path('accounting/', include('accounting.urls')),
    path('human_resources/', include('human_resources.urls')),
    path('marketing_automation/', include('marketing_automation.urls')),
    path('coche/<int:coche_id>/', website_views.coche_detalle, name='website_coche_detalle'),
    path('contacto/', website_views.contacto, name='contacto'),
]