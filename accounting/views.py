from django.shortcuts import render, redirect
from .models import Cuenta
from .forms import CuentaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from accounts.views import get_user_roles
from django.db.models import Sum
from decimal import Decimal

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

@login_required
def contabilidad(request):
    # Obtener parámetros de filtrado
    tipo = request.GET.get('tipo')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    orden = request.GET.get('orden', '-fecha')

    # Filtrar cuentas
    cuentas = Cuenta.objects.all()
    if tipo:
        cuentas = cuentas.filter(tipo=tipo)
    if fecha_inicio:
        cuentas = cuentas.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        cuentas = cuentas.filter(fecha__lte=fecha_fin)
    
    # Ordenar resultados
    cuentas = cuentas.order_by(orden)

    # Calcular totales
    balance_total = Cuenta.get_balance_total()
    ingresos_mes = Cuenta.get_ingresos_mes()
    gastos_mes = Cuenta.get_gastos_mes()

    context = {
        'cuentas': cuentas,
        'balance_total': balance_total,
        'ingresos_mes': ingresos_mes,
        'gastos_mes': gastos_mes,
        'tipos': dict(Cuenta.TIPOS),
        'filtros': {
            'tipo': tipo,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
        }
    }
    return render(request, 'accounting/contabilidad.html', context)

@login_required
@role_required(['Contabilidad'])
def dashboard(request):
    return render(request, 'accounting/dashboard.html')

@login_required
@role_required(['Contabilidad'])
def ingresos(request):
    return render(request, 'accounting/ingresos.html')

@login_required
@role_required(['Contabilidad'])
def gastos(request):
    return render(request, 'accounting/gastos.html')

@login_required
@role_required(['Contabilidad'])
def balance(request):
    return render(request, 'accounting/balance.html')

@login_required
@role_required(['Contabilidad'])
def facturas(request):
    return render(request, 'accounting/facturas.html')

@login_required
@role_required(['Contabilidad'])
def crear_factura(request):
    return render(request, 'accounting/crear_factura.html')
