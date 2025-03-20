from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
from .models import OrdenFabricacion, ComponenteOrden
from .forms import OrdenFabricacionForm
from accounts.decorators import role_required
from django.db.models.deletion import ProtectedError
from django.db.models.fields import DecimalField
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField
from ecommerce.models import Coche, Pedido
from inventory.models import Componente, Stock, MovimientoStock
from sales.models import Pedido as SalesPedido
from inventory.models import OrdenEntrega
from accounting.models import Cuenta, Factura, Balance

@login_required
@role_required(['Produccion'])
def manufacturing_produccion(request):
    return render(request, 'manufacturing/produccion.html')

@login_required
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenFabricacion, id=orden_id)
    pedido_info = {}
    
    if orden.pedido:
        pedido_info = {
            'id': orden.pedido.id,
            'cliente': orden.pedido.cliente,
            'coche': orden.pedido.coche,
            'rueda': orden.pedido.rueda,
            'color': orden.pedido.color,
            'estado': orden.pedido.estado
        }
        
        if request.method == 'POST':
            accion = request.POST.get('accion')
            
            if accion == 'asignar_ruedas' and not orden.ruedas_disponibles:
                try:
                    ruedas = Componente.objects.get(tipo=f'ruedas_{orden.pedido.rueda.replace('"', "")}')
                    stock_ruedas = Stock.objects.filter(componente=ruedas, cantidad__gt=0).first()
                    if stock_ruedas:
                        stock_ruedas.cantidad -= 1
                        stock_ruedas.save()
                        orden.ruedas_asignadas = ruedas
                        orden.ruedas_disponibles = True
                        messages.success(request, f'Se han asignado ruedas de tipo {orden.pedido.rueda}')
                    else:
                        messages.warning(request, f'No se encontraron ruedas de tipo {orden.pedido.rueda} en stock')
                except Componente.DoesNotExist:
                    messages.warning(request, f'No se encontró el componente de ruedas tipo {orden.pedido.rueda}')
            
            elif accion == 'asignar_motor' and not orden.motorizacion_disponible:
                try:
                    motor = Componente.objects.get(tipo='motor_v6')
                    stock_motor = Stock.objects.filter(componente=motor, cantidad__gt=0).first()
                    if stock_motor:
                        stock_motor.cantidad -= 1
                        stock_motor.save()
                        orden.motorizacion_asignada = motor
                        orden.motorizacion_disponible = True
                        messages.success(request, 'Se ha asignado el motor estándar')
                    else:
                        messages.warning(request, 'No se encontró motor estándar en stock')
                except Componente.DoesNotExist:
                    messages.warning(request, 'No se encontró el componente de motor estándar')
            
            elif accion == 'asignar_tapiceria' and not orden.tapiceria_disponible:
                try:
                    color_mapping = {
                        'Negro': 'tapiceria_cuero_negro',
                        'Rojo': 'tapiceria_alcantara',
                        'Azul': 'tapiceria_tela',
                        'Blanco': 'tapiceria_tela'
                    }
                    tipo_tapiceria = color_mapping.get(orden.pedido.color, 'tapiceria_tela')
                    tapiceria = Componente.objects.get(tipo=tipo_tapiceria)
                    stock_tapiceria = Stock.objects.filter(componente=tapiceria, cantidad__gt=0).first()
                    if stock_tapiceria:
                        stock_tapiceria.cantidad -= 1
                        stock_tapiceria.save()
                        orden.tapiceria_asignada = tapiceria
                        orden.tapiceria_disponible = True
                        messages.success(request, f'Se ha asignado tapicería para color {orden.pedido.color}')
                    else:
                        messages.warning(request, f'No se encontró tapicería para color {orden.pedido.color} en stock')
                except Componente.DoesNotExist:
                    messages.warning(request, f'No se encontró el componente de tapicería para color {orden.pedido.color}')
            
            elif accion == 'asignar_extras' and not orden.extras_disponibles:
                try:
                    extras = Componente.objects.get(tipo='extra_techo')
                    stock_extras = Stock.objects.filter(componente=extras, cantidad__gt=0).first()
                    if stock_extras:
                        stock_extras.cantidad -= 1
                        stock_extras.save()
                        orden.extras_asignados = extras
                        orden.extras_disponibles = True
                        messages.success(request, 'Se han asignado los extras básicos')
                    else:
                        messages.warning(request, 'No se encontraron extras básicos en stock')
                except Componente.DoesNotExist:
                    messages.warning(request, 'No se encontró el componente de extras básicos')
            
            elif accion == 'iniciar_produccion':
                if orden.ruedas_disponibles and orden.motorizacion_disponible and orden.tapiceria_disponible and orden.extras_disponibles:
                    orden.estado = 'en_proceso'
                    messages.success(request, 'Se ha iniciado la fabricación del vehículo')
                else:
                    messages.error(request, 'No se puede iniciar la fabricación hasta que todos los componentes estén asignados')
            
            elif accion == 'finalizar_produccion':
                orden.estado = 'completada'
                orden.fecha_fin = timezone.now()
                messages.success(request, 'Se ha finalizado la fabricación del vehículo')
            
            elif accion == 'entregar_vehiculo':
                if orden.estado == 'completada':
                    if not OrdenEntrega.objects.filter(pedido=orden.pedido).exists():
                        orden_entrega = OrdenEntrega.objects.create(
                            pedido=orden.pedido,
                            estado='entregado'
                        )
                        if orden.pedido:
                            orden.pedido.estado = 'entregado'
                            orden.pedido.save()
                        messages.success(request, 'Vehículo entregado al cliente exitosamente.')
                    else:
                        if orden.pedido:
                            orden.pedido.estado = 'entregado'
                            orden.pedido.save()
                        messages.success(request, 'Vehículo entregado al cliente exitosamente.')
                else:
                    messages.error(request, 'El vehículo debe estar completado antes de entregarlo.')
            
            orden.save()
            
    else:
        messages.warning(request, 'Esta orden no tiene un pedido asociado')
    
    # Verificar si todos los componentes están asignados
    todos_componentes_asignados = (
        orden.ruedas_disponibles and 
        orden.motorizacion_disponible and 
        orden.tapiceria_disponible and 
        orden.extras_disponibles
    )
    
    return render(request, 'manufacturing/detalle_orden.html', {
        'orden': orden,
        'pedido_info': pedido_info,
        'todos_componentes_asignados': todos_componentes_asignados
    })

@login_required
def lista_ordenes(request):
    ordenes = OrdenFabricacion.objects.all().order_by('-fecha_inicio')
    return render(request, 'manufacturing/ordenes_fabricacion.html', {'ordenes': ordenes})

@login_required
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenFabricacionForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.fecha_inicio = timezone.now()
            orden.save()
            messages.success(request, 'Orden de fabricación creada exitosamente.')
            return redirect('manufacturing:detalle_orden', orden.id)
    else:
        form = OrdenFabricacionForm()
    
    return render(request, 'manufacturing/crear_orden.html', {'form': form})

@login_required
def editar_orden(request, orden_id):
    orden = get_object_or_404(OrdenFabricacion, id=orden_id)
    
    if request.method == 'POST':
        form = OrdenFabricacionForm(request.POST, instance=orden)
        if form.is_valid():
            orden = form.save()
            messages.success(request, 'Orden de fabricación actualizada exitosamente.')
            return redirect('manufacturing:detalle_orden', orden.id)
    else:
        form = OrdenFabricacionForm(instance=orden)
    
    return render(request, 'manufacturing/editar_orden.html', {
        'form': form,
        'orden': orden
    })

@login_required
def eliminar_orden(request, orden_id):
    orden = get_object_or_404(OrdenFabricacion, id=orden_id)
    
    try:
        orden.delete()
        messages.success(request, 'Orden de fabricación eliminada exitosamente.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar esta orden porque tiene registros asociados.')
    
    return redirect('manufacturing:lista_ordenes') 