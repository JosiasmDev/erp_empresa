from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.decorators import role_required
from decimal import Decimal
from django.db import transaction

from .models import MovimientoStock, Stock
from .forms import MovimientoStockForm
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
    if request.method == 'POST':
        form = MovimientoStockForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                movimiento = form.save(commit=False)
                movimiento.usuario = request.user
                
                # Calcular el costo unitario como 30% del precio de venta
                componente = movimiento.componente
                movimiento.costo_unitario = Decimal(str(float(componente.precio_compra) * 0.3))
                
                # Calcular el precio total
                cantidad = Decimal(str(movimiento.cantidad))
                movimiento.precio_total = movimiento.costo_unitario * cantidad
                
                # Crear orden de compra
                orden_compra = OrdenCompra.objects.create(
                    proveedor=Proveedor.objects.first(),  # Deberías seleccionar el proveedor adecuado
                    estado='pendiente',
                    total=movimiento.precio_total
                )
                
                # Crear detalle de orden de compra
                DetalleOrdenCompra.objects.create(
                    orden=orden_compra,
                    componente=componente,
                    cantidad=cantidad,
                    precio_unitario=movimiento.costo_unitario
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
                
                # Actualizar el stock
                stock, created = Stock.objects.get_or_create(componente=componente)
                if movimiento.tipo == 'entrada':
                    stock.cantidad += movimiento.cantidad
                elif movimiento.tipo == 'salida':
                    stock.cantidad -= movimiento.cantidad
                stock.save()
                
                messages.success(
                    request, 
                    f'Movimiento registrado exitosamente. Precio total: {movimiento.precio_total}€. '
                    f'Se ha generado la orden de compra #{orden_compra.id} y la factura #{factura.numero}'
                )
                return redirect('purchase:detalle_orden_compra', orden_compra.id)
    else:
        form = MovimientoStockForm()
    return render(request, 'inventory/crear_movimiento.html', {'form': form})

@login_required
def gestionar_stock(request):
    from manufacturing.models import Componente
    from .models import Stock, MovimientoStock
    
    # Obtener todos los componentes con su stock
    stocks = Stock.objects.all().select_related('componente')
    
    # Obtener los últimos movimientos
    ultimos_movimientos = MovimientoStock.objects.all().select_related('componente')[:10]
    
    # Obtener componentes por categoría
    ruedas = Componente.objects.filter(tipo__startswith='ruedas_')
    motores = Componente.objects.filter(tipo__startswith='motor_')
    tapicerias = Componente.objects.filter(tipo__startswith='tapiceria_')
    extras = Componente.objects.filter(tipo__startswith='extra_')
    
    # Obtener todos los proveedores
    proveedores = Proveedor.objects.all()
    
    # Calcular alertas de stock bajo
    alertas_stock = []
    for stock in stocks:
        if stock.cantidad <= stock.stock_minimo:
            alertas_stock.append({
                'componente': stock.componente,
                'stock_actual': stock.cantidad,
                'stock_minimo': stock.stock_minimo,
                'diferencia': stock.stock_minimo - stock.cantidad,
                'precio_venta': stock.componente.precio_compra  # Este es realmente el precio de venta
            })
    
    # Preparar el contexto con los precios de venta
    stocks_con_precios = []
    for stock in stocks:
        stocks_con_precios.append({
            'id': stock.id,
            'componente': stock.componente,
            'cantidad': stock.cantidad,
            'stock_minimo': stock.stock_minimo,
            'stock_maximo': stock.stock_maximo,
            'ubicacion': stock.ubicacion,
            'notas': stock.notas,
            'precio_venta': stock.componente.precio_compra  # Este es realmente el precio de venta
        })
    
    context = {
        'stocks': stocks_con_precios,
        'ultimos_movimientos': ultimos_movimientos,
        'ruedas': ruedas,
        'motores': motores,
        'tapicerias': tapicerias,
        'extras': extras,
        'proveedores': proveedores,
        'alertas_stock': alertas_stock,
    }
    return render(request, 'inventory/gestionar_stock.html', context)

@login_required
def editar_stock(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id')
        try:
            stock = Stock.objects.get(id=stock_id)
            stock.stock_minimo = request.POST.get('stock_minimo')
            stock.stock_maximo = request.POST.get('stock_maximo')
            stock.ubicacion = request.POST.get('ubicacion')
            stock.notas = request.POST.get('notas')
            stock.save()
            messages.success(request, 'Stock actualizado exitosamente.')
        except Stock.DoesNotExist:
            messages.error(request, 'No se encontró el stock especificado.')
    return redirect('inventory_stock')

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