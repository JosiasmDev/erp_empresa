from django.shortcuts import render, redirect
from .models import Cuenta
from .forms import CuentaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from accounts.views import get_user_roles

@role_required(['accounting'])
def accounting_facturas(request):
    cuentas = Cuenta.objects.all()
    return render(request, 'accounting/facturas.html', {'cuentas': cuentas})

@login_required
def facturas_view(request):
    """Vista de facturas con permisos y datos correctos."""
    cuentas = Cuenta.objects.all()
    context = {
        'cuentas': cuentas,
        **get_user_roles(request.user)
    }
    return render(request, 'accounting/facturas.html', context)

@login_required
def crear_factura(request):
    """Vista para crear una nueva cuenta"""
    roles_context = get_user_roles(request.user)
    
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada.')
            return redirect('accounting_facturas')
    else:
        form = CuentaForm()
    
    return render(request, 'accounting/crear_factura.html', {'form': form, **roles_context})
