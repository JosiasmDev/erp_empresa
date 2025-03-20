from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import OrdenCompra, DetalleOrdenCompra, Proveedor

@login_required
def listar_ordenes_compra(request):
    ordenes = OrdenCompra.objects.all().order_by('-fecha')
    return render(request, 'purchase/ordenes_compra.html', {
        'ordenes': ordenes,
        'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
        'is_cliente': request.user.groups.filter(name='Clientes').exists(),
        'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
        'is_compras': request.user.groups.filter(name='Compras').exists(),
        'is_logistica': request.user.groups.filter(name='Logistica').exists(),
    })

@login_required
def crear_orden_compra(request):
    if request.method == 'POST':
        componente_id = request.POST.get('componente_id')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')
        proveedor_id = request.POST.get('proveedor_id')
        
        from manufacturing.models import Componente
        componente = get_object_or_404(Componente, id=componente_id)
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        
        # Crear orden de compra
        orden_compra = OrdenCompra.objects.create(
            proveedor=proveedor,
            estado='pendiente',
            total=0  # Se actualizará automáticamente al crear el detalle
        )
        
        # Crear detalle de orden
        DetalleOrdenCompra.objects.create(
            orden=orden_compra,
            componente=componente,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        
        messages.success(request, 'Orden de compra creada correctamente.')
        return redirect('purchase:detalle_orden_compra', orden_compra.id)
    
    return redirect('inventory:inventory_stock')

@login_required
def detalle_orden_compra(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    detalles = orden.detalleordencompra_set.all()
    return render(request, 'purchase/detalle_orden_compra.html', {
        'orden': orden,
        'detalles': detalles,
        'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
        'is_cliente': request.user.groups.filter(name='Clientes').exists(),
        'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
        'is_compras': request.user.groups.filter(name='Compras').exists(),
        'is_logistica': request.user.groups.filter(name='Logistica').exists(),
    })

@login_required
def aprobar_orden(request, orden_id):
    if request.method == 'POST':
        with transaction.atomic():
            orden = get_object_or_404(OrdenCompra, id=orden_id)
            if orden.estado == 'pendiente':
                # Actualizar estado de la orden
                orden.estado = 'aprobada'
                orden.save()
                
                # Actualizar factura asociada
                from accounting.models import Factura, Cuenta, Balance
                factura = Factura.objects.filter(orden_compra=orden).first()
                if factura:
                    factura.estado = 'pagada'
                    factura.save()
                
                # Actualizar cuenta asociada
                cuenta = Cuenta.objects.filter(orden_compra=orden).first()
                if cuenta:
                    cuenta.tipo = 'compra'  # Asegurarnos que es tipo compra
                    cuenta.save()
                
                # Actualizar balance
                balance = Balance.objects.create()
                balance.calcular_totales()
                balance.save()
                
                messages.success(request, 'Orden de compra aprobada y factura pagada correctamente.')
            return redirect('inventory:stock')
    return redirect('purchase:ordenes_compra')

@login_required
def rechazar_orden(request, orden_id):
    if request.method == 'POST':
        orden = get_object_or_404(OrdenCompra, id=orden_id)
        if orden.estado == 'pendiente':
            orden.estado = 'rechazada'
            orden.save()
            messages.success(request, 'Orden de compra rechazada.')
        return redirect('purchase:detalle_orden_compra', orden.id)
    return redirect('purchase:ordenes_compra')