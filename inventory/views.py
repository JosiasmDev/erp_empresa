from django.shortcuts import render, redirect, get_object_or_404
from .models import MovimientoStock
from .forms import MovimientoStockForm
from django.contrib import messages
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required
from .models import Stock, Componente
from .forms import StockForm

@role_required(['inventory'])
def inventory_stock(request):
    from inventory.models import MovimientoStock
    movimientos = MovimientoStock.objects.all()
    return render(request, 'inventory/stock.html', {'movimientos': movimientos})

def stock(request):
    movimientos = MovimientoStock.objects.all()
    return render(request, 'inventory/stock.html', {'movimientos': movimientos})

def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoStockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento registrado.')
            return redirect('inventory_stock')
    else:
        form = MovimientoStockForm()
    return render(request, 'inventory/crear_movimiento.html', {'form': form})

@login_required
def gestionar_stock(request):
    stocks = Stock.objects.all().select_related('componente')
    return render(request, 'inventory/gestionar_stock.html', {'stocks': stocks})

@login_required
def editar_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock = form.save()
            messages.success(request, 'Stock actualizado correctamente')
            return redirect('inventory:gestionar_stock')
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