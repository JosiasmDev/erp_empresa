from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import OrdenFabricacion, Componente, ComponenteOrden
from .forms import OrdenFabricacionForm
from accounts.decorators import role_required
from django.utils import timezone
from decimal import Decimal
from accounting.models import Cuenta
from datetime import datetime, timedelta

@login_required
@role_required(['Produccion'])
def manufacturing_produccion(request):
    ordenes_list = OrdenFabricacion.objects.all().order_by('-fecha_inicio')  # Añadimos ordenamiento por fecha_inicio descendente
    paginator = Paginator(ordenes_list, 10)  # Muestra 10 órdenes por página
    page_number = request.GET.get('page')
    ordenes = paginator.get_page(page_number)
    
    context = {
        'ordenes': ordenes,
        'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
        'is_cliente': request.user.groups.filter(name='Clientes').exists(),
        'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
        'is_compras': request.user.groups.filter(name='Compras').exists(),
        'is_logistica': request.user.groups.filter(name='Logistica').exists(),
    }
    return render(request, 'manufacturing/produccion.html', context)

@login_required
@role_required(['Produccion'])
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenFabricacionForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.estado = 'pendiente'
            orden.save()
            messages.success(request, 'Orden de fabricación creada exitosamente.')
            return redirect('manufacturing:ordenes_fabricacion')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = OrdenFabricacionForm()
    
    return render(request, 'manufacturing/crear_orden.html', {'form': form})

@login_required
@role_required(['Produccion'])
def ordenes_fabricacion(request):
    ordenes = OrdenFabricacion.objects.all()
    return render(request, 'manufacturing/ordenes_fabricacion.html', {'ordenes': ordenes})

@login_required
@role_required(['Produccion'])
def detalle_orden(request, orden_id):
    orden = OrdenFabricacion.objects.get(id=orden_id)
    if not orden.fecha_inicio:
        orden.fecha_inicio = datetime.now()
        orden.fecha_fin = orden.fecha_inicio + timedelta(days=14)  # 2 semanas para la fabricación
        orden.save()
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'iniciar_produccion' and orden.verificar_componentes():
            orden.estado = 'en_proceso'
            orden.fecha_inicio = timezone.now()
            orden.save()
            messages.success(request, 'Producción iniciada exitosamente.')
            
        elif accion == 'finalizar_produccion':
            orden.estado = 'completada'
            orden.fecha_fin = timezone.now()
            orden.save()
            
            # Actualizar el pedido
            orden.pedido.estado = 'completado'
            orden.pedido.save()
            
            messages.success(request, 'Producción finalizada exitosamente.')
            
        elif accion == 'solicitar_componente':
            componente_id = request.POST.get('componente_id')
            componente = get_object_or_404(Componente, id=componente_id)
            
            # Calcular el costo (30% del precio de venta)
            costo = orden.pedido.precio_total * Decimal('0.30')
            
            # Registrar el gasto en contabilidad
            Cuenta.objects.create(
                tipo='compra',
                descripcion=f'Compra de componentes para orden {orden.numero_orden}',
                monto=costo,
                orden_compra=None
            )
            
            # Marcar el componente como disponible
            if componente.nombre == 'Ruedas':
                orden.ruedas_disponibles = True
            elif componente.nombre == 'Motorizacion':
                orden.motorizacion_disponible = True
            elif componente.nombre == 'Tapiceria':
                orden.tapiceria_disponible = True
            elif componente.nombre == 'Extras':
                orden.extras_disponibles = True
            
            orden.save()
            messages.success(request, f'Componente {componente.nombre} solicitado exitosamente.')
    
    return render(request, 'manufacturing/detalle_orden.html', {'orden': orden})