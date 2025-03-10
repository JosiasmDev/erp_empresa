# ecommerce/views.py
from django.shortcuts import render
from .models import Coche

def ecommerce_dashboard(request):
    coches = Coche.objects.all()
    context = {
        'coches': coches,
        'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
        'is_cliente': request.user.groups.filter(name='Clientes').exists(),
        'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
        'is_compras': request.user.groups.filter(name='Compras').exists(),
        'is_logistica': request.user.groups.filter(name='Logistica').exists(),
    }
    return render(request, 'ecommerce/dashboard.html', context)