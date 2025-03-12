from django.shortcuts import render, redirect
from .models import Factura
from .forms import FacturaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required

@role_required(['accounting'])
def accounting_facturas(request):
    from accounting.models import Factura
    facturas = Factura.objects.all()
    return render(request, 'accounting/facturas.html', {'facturas': facturas})

@login_required
def facturas_view(request):
    """Vista de facturas con permisos y datos correctos."""
    facturas = Factura.objects.all()
    roles_context = get_user_roles(request.user)  # Obtener roles del usuario

    print(f"Roles del usuario: {roles_context['roles']}")  # Depuración de roles

    # Agregar los roles al contexto para la plantilla
    context = {
        'facturas': facturas,
        **roles_context  # Incluye roles en el contexto
    }
    return render(request, 'accounting/facturas.html', context)


def get_user_roles(user):
    """Devuelve los roles de un usuario (esto debe ajustarse según tu modelo)."""
    roles = []
    if user.is_superuser:
        roles.append('Administrador')  # Si es superusuario, es un administrador
    # Aquí podrías agregar otros roles según tus necesidades
    return {'roles': roles}  # Devuelve los roles del usuario

def crear_factura(request):
    """Vista para crear una nueva factura"""
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Factura creada.')
            return redirect('accounting_facturas')
    else:
        form = FacturaForm()

    roles_context = get_user_roles(request.user)  # Obtener roles del usuario
    return render(request, 'accounting/crear_factura.html', {'form': form, **roles_context})
