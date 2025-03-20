from django.shortcuts import render, redirect
from .models import Cuenta, Factura, Balance
from .forms import CuentaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from accounts.views import get_user_roles
from django.db.models import Sum, Q
from decimal import Decimal
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils.safestring import mark_safe
from human_resources.models import Empleado

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
@role_required(['Contabilidad', 'Administrador'])
def dashboard(request):
    # Obtener datos del mes actual
    inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
    
    # Calcular totales del mes
    facturas_compra = Factura.objects.filter(
        tipo='compra',
        estado='pagada',
        fecha__range=(inicio_mes, fin_mes)
    )
    facturas_venta = Factura.objects.filter(
        tipo='venta',
        estado='pagada',
        fecha__range=(inicio_mes, fin_mes)
    )
    
    compras_mes = facturas_compra.aggregate(total=Sum('total'))['total'] or Decimal('0')
    ventas_mes = facturas_venta.aggregate(total=Sum('total'))['total'] or Decimal('0')
    
    # Obtener últimas facturas
    ultimas_facturas = Factura.objects.filter(estado='pagada').order_by('-fecha')[:5]
    
    # Obtener cuentas del mes
    cuentas_mes = Cuenta.objects.filter(fecha__range=(inicio_mes, fin_mes))
    ingresos_mes = cuentas_mes.filter(tipo__in=['ingreso', 'venta']).aggregate(total=Sum('monto'))['total'] or Decimal('0')
    gastos_mes = cuentas_mes.filter(tipo__in=['gasto', 'compra', 'salario']).aggregate(total=Sum('monto'))['total'] or Decimal('0')
    
    context = {
        'compras_mes': compras_mes,
        'ventas_mes': ventas_mes,
        'ingresos_mes': ingresos_mes,
        'gastos_mes': gastos_mes,
        'balance_mes': ingresos_mes - gastos_mes,
        'ultimas_facturas': ultimas_facturas,
        'is_contabilidad': True,
    }
    return render(request, 'accounting/dashboard.html', context)

@login_required
@role_required(['Contabilidad', 'Administrador'])
def ingresos(request):
    # Obtener todas las facturas de venta pagadas
    facturas = Factura.objects.filter(tipo='venta', estado='pagada').order_by('-fecha')
    total_ingresos = facturas.aggregate(total=Sum('total'))['total'] or Decimal('0')
    
    # Obtener todos los ingresos de cuentas
    cuentas_ingresos = Cuenta.objects.filter(tipo__in=['ingreso', 'venta'])
    total_cuentas = cuentas_ingresos.aggregate(total=Sum('monto'))['total'] or Decimal('0')
    
    context = {
        'facturas': facturas,
        'cuentas': cuentas_ingresos,
        'total_ingresos': total_ingresos + total_cuentas,
        'is_contabilidad': True,
    }
    return render(request, 'accounting/ingresos.html', context)

@login_required
@role_required(['Contabilidad', 'Administrador'])
def gastos(request):
    # Obtener todas las facturas de compra pagadas
    facturas = Factura.objects.filter(tipo='compra', estado='pagada').order_by('-fecha')
    total_facturas = facturas.aggregate(total=Sum('total'))['total'] or Decimal('0')
    
    # Obtener todos los gastos de cuentas
    cuentas_gastos = Cuenta.objects.filter(tipo__in=['gasto', 'compra', 'salario'])
    total_cuentas = cuentas_gastos.aggregate(total=Sum('monto'))['total'] or Decimal('0')
    
    context = {
        'facturas': facturas,
        'cuentas': cuentas_gastos,
        'total_gastos': total_facturas + total_cuentas,
        'is_contabilidad': True,
    }
    return render(request, 'accounting/gastos.html', context)

@login_required
@role_required(['Contabilidad', 'Administrador'])
def balance(request):
    # Obtener datos del mes actual
    inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
    
    # Obtener datos de los últimos 6 meses para gráficas
    meses = []
    ingresos_mensuales = []
    gastos_mensuales = []
    gastos_sueldos = []
    
    for i in range(5, -1, -1):
        fecha = inicio_mes - timedelta(days=30*i)
        mes_inicio = fecha.replace(day=1)
        mes_fin = (mes_inicio + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
        
        meses.append(fecha.strftime('%B %Y'))
        
        # Calcular ingresos del mes
        ingresos = Cuenta.objects.filter(
            tipo__in=['ingreso', 'venta'],
            fecha__range=(mes_inicio, mes_fin)
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')
        ingresos_mensuales.append(float(ingresos))
        
        # Calcular gastos del mes (excluyendo sueldos)
        gastos = Cuenta.objects.filter(
            tipo__in=['gasto', 'compra'],
            fecha__range=(mes_inicio, mes_fin)
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')
        gastos_mensuales.append(float(gastos))
        
        # Calcular gastos de sueldos del mes
        sueldos = Cuenta.objects.filter(
            tipo='salario',
            fecha__range=(mes_inicio, mes_fin)
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')
        gastos_sueldos.append(float(sueldos))
    
    # Obtener datos del mes actual
    cuentas_mes = Cuenta.objects.filter(fecha__range=(inicio_mes, fin_mes))
    ingresos_mes = cuentas_mes.filter(tipo__in=['ingreso', 'venta']).aggregate(total=Sum('monto'))['total'] or Decimal('0')
    gastos_mes = cuentas_mes.filter(tipo__in=['gasto', 'compra']).aggregate(total=Sum('monto'))['total'] or Decimal('0')
    sueldos_mes = cuentas_mes.filter(tipo='salario').aggregate(total=Sum('monto'))['total'] or Decimal('0')
    
    # Obtener distribución de gastos por tipo
    gastos_por_tipo = []
    for tipo in ['gasto', 'compra']:
        total = cuentas_mes.filter(tipo=tipo).aggregate(total=Sum('monto'))['total'] or Decimal('0')
        if total > 0:
            gastos_por_tipo.append({
                'tipo': tipo,
                'total': float(total)
            })
    
    # Agregar sueldos a la distribución de gastos
    if sueldos_mes > 0:
        gastos_por_tipo.append({
            'tipo': 'salario',
            'total': float(sueldos_mes)
        })
    
    # Obtener distribución de ingresos por tipo
    ingresos_por_tipo = []
    for tipo in ['ingreso', 'venta']:
        total = cuentas_mes.filter(tipo=tipo).aggregate(total=Sum('monto'))['total'] or Decimal('0')
        if total > 0:
            ingresos_por_tipo.append({
                'tipo': tipo,
                'total': float(total)
            })
    
    # Obtener desglose de sueldos por cargo
    sueldos_por_departamento = []
    cargos = Empleado.objects.values('cargo').distinct()
    for cargo in cargos:
        # Primero obtenemos los empleados con este cargo
        empleados_cargo = Empleado.objects.filter(cargo=cargo['cargo']).values_list('id', flat=True)
        # Luego sumamos los sueldos de las cuentas asociadas a estos empleados
        total_cargo = Cuenta.objects.filter(
            tipo='salario',
            fecha__range=(inicio_mes, fin_mes),
            empleado_id__in=empleados_cargo
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')
        
        if total_cargo > 0:
            sueldos_por_departamento.append({
                'departamento': cargo['cargo'],  # Usamos el cargo como "departamento" para mantener la estructura
                'total': float(total_cargo)
            })
    
    # Calcular ratios financieros
    total_gastos_mes = gastos_mes + sueldos_mes
    ratio_liquidez = float(ingresos_mes) / float(total_gastos_mes) if total_gastos_mes > 0 else 0
    
    # Serializar datos para JavaScript
    datos_js = {
        'meses': meses,
        'ingresos_mensuales': ingresos_mensuales,
        'gastos_mensuales': gastos_mensuales,
        'gastos_sueldos': gastos_sueldos,
        'gastos_por_tipo': gastos_por_tipo,
        'ingresos_por_tipo': ingresos_por_tipo,
        'sueldos_por_departamento': sueldos_por_departamento
    }
    
    context = {
        'datos_graficas': mark_safe(json.dumps(datos_js)),
        'ingresos_mes': ingresos_mes,
        'gastos_mes': gastos_mes,
        'sueldos_mes': sueldos_mes,
        'total_gastos_mes': total_gastos_mes,
        'balance_mes': ingresos_mes - total_gastos_mes,
        'ratio_liquidez': ratio_liquidez,
        'is_contabilidad': True,
    }
    
    return render(request, 'accounting/balance_temp.html', context)

@login_required
@role_required(['Contabilidad', 'Administrador'])
def facturas(request):
    facturas = Factura.objects.all().order_by('-fecha')
    context = {
        'facturas': facturas,
        'is_contabilidad': True,
    }
    return render(request, 'accounting/facturas.html', context)

@login_required
@role_required(['Contabilidad', 'Administrador'])
def crear_factura(request):
    if request.method == 'POST':
        # Lógica para crear factura manual
        pass
    return render(request, 'accounting/crear_factura.html', {'is_contabilidad': True})
