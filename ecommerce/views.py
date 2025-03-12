# ecommerce/views.py
from django.shortcuts import render
from .models import Coche
from accounts.decorators import role_required

@role_required(['ecommerce'])
def ecommerce_dashboard(request):
    from ecommerce.models import Coche
    coches = Coche.objects.all()
    return render(request, 'ecommerce/dashboard.html', {'coches': coches})

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