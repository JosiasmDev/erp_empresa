from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrdenCompra, DetalleOrdenCompra, Proveedor
from manufacturing.models import Componente

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
    
    return redirect('inventory:gestionar_stock')

@login_required
def detalle_orden_compra(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    detalles = orden.detalles.all()
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
        orden = get_object_or_404(OrdenCompra, id=orden_id)
        if orden.estado == 'pendiente':
            orden.estado = 'aprobada'
            orden.save()
            messages.success(request, 'Orden de compra aprobada correctamente.')
        return redirect('purchase:detalle_orden_compra', orden.id)
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