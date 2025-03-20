from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.decorators import role_required
from decimal import Decimal
from django.db import transaction

from .models import MovimientoStock, Stock, Componente
from .forms import MovimientoStockForm, StockForm
from purchase.models import Proveedor, OrdenCompra, DetalleOrdenCompra
from accounting.models import Cuenta, Factura, Balance

@role_required(['inventory'])
def inventory_stock(request):
    movimientos = MovimientoStock.objects.all()
    return render(request, 'inventory/stock.html', {'movimientos': movimientos})

def stock(request):
    movimientos = MovimientoStock.objects.all()
    return render(request, 'inventory/stock.html', {'movimientos': movimientos})

@login_required
def crear_movimiento(request):
    componente_id = request.GET.get('componente')
    if componente_id:
        componente = get_object_or_404(Componente, id=componente_id)
        initial = {'componente': componente}
    else:
        initial = {}
        componente = None

    if request.method == 'POST':
        form = MovimientoStockForm(request.POST, initial=initial)
        if form.is_valid():
            with transaction.atomic():
                movimiento = form.save(commit=False)
                movimiento.usuario = request.user
                
                # Usar el precio de compra calculado automáticamente (30% del precio de venta)
                componente = movimiento.componente
                movimiento.precio_unitario = componente.precio_compra
                
                # Calcular el precio total
                cantidad = Decimal(str(movimiento.cantidad))
                movimiento.precio_total = movimiento.precio_unitario * cantidad
                
                # Obtener o crear el proveedor por defecto
                proveedor, created = Proveedor.objects.get_or_create(
                    nombre='Proveedor Principal',
                    defaults={
                        'direccion': 'Calle Principal 123',
                        'telefono': '123456789',
                        'email': 'juan.perez@proveedor.com',
                        'activo': True
                    }
                )
                
                # Crear orden de compra
                orden_compra = OrdenCompra.objects.create(
                    proveedor=proveedor,
                    estado='pendiente',
                    total=movimiento.precio_total
                )
                
                # Crear detalle de orden de compra
                DetalleOrdenCompra.objects.create(
                    orden=orden_compra,
                    componente=componente,
                    cantidad=movimiento.cantidad,
                    precio_unitario=movimiento.precio_unitario
                )
                
                # Crear registro contable
                cuenta = Cuenta.objects.create(
                    tipo='compra',
                    descripcion=f'Compra de {cantidad} unidades de {componente.nombre}',
                    monto=movimiento.precio_total,
                    orden_compra=orden_compra
                )
                
                # Crear factura
                factura = Factura.objects.create(
                    tipo='compra',
                    descripcion=f'Compra de {cantidad} unidades de {componente.nombre}',
                    subtotal=movimiento.precio_total / Decimal('1.21'),  # Precio sin IVA
                    orden_compra=orden_compra,
                    cuenta=cuenta
                )
                
                # Actualizar balance
                balance = Balance.objects.create()
                balance.calcular_totales()
                balance.save()
                
                movimiento.save()
                
                messages.success(
                    request, 
                    f'Movimiento registrado exitosamente. Precio total: {movimiento.precio_total}€. '
                    f'Se ha generado la orden de compra #{orden_compra.id} y la factura #{factura.numero}'
                )
                return redirect('purchase:detalle_orden_compra', orden_compra.id)
    else:
        form = MovimientoStockForm(initial=initial)
    
    return render(request, 'inventory/crear_movimiento.html', {
        'form': form,
        'componente': componente
    })

@login_required
def gestionar_stock(request):
    stocks = Stock.objects.select_related('componente').order_by('componente__tipo', 'componente__nombre')
    return render(request, 'inventory/gestionar_stock.html', {'stocks': stocks})

@login_required
def editar_stock(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock = form.save()
            messages.success(request, 'Stock actualizado exitosamente.')
            return redirect('inventory:stock')
    else:
        form = StockForm(instance=stock)
    
    return render(request, 'inventory/editar_stock.html', {
        'form': form,
        'stock': stock
    })

@login_required
def verificar_stock(request, orden_fabricacion_id):
    """Verifica el stock necesario para una orden de fabricación"""
    from manufacturing.models import OrdenFabricacion
    from purchase.models import OrdenCompra
    
    orden = get_object_or_404(OrdenFabricacion, id=orden_fabricacion_id)
    componentes_necesarios = orden.componentes.all()
    
    stock_insuficiente = []
    for componente in componentes_necesarios:
        stock = Stock.objects.filter(componente=componente).first()
        if not stock or stock.cantidad < componente.cantidad:
            stock_insuficiente.append(componente)
    
    if stock_insuficiente:
        # Crear orden de compra
        orden_compra = OrdenCompra.objects.create(
            estado='pendiente',
            total=sum(c.precio_compra * c.cantidad for c in stock_insuficiente)
        )
        
        messages.warning(request, 'Stock insuficiente. Se ha generado una orden de compra.')
        return redirect('purchase:detalle_orden_compra', orden_compra.id)
    
    messages.success(request, 'Stock suficiente para la orden de fabricación.')
    return redirect('manufacturing:detalle_orden_fabricacion', orden.id)

@login_required
def get_proveedores(request):
    proveedores = Proveedor.objects.all()
    return JsonResponse([{'id': p.id, 'nombre': p.nombre} for p in proveedores], safe=False)