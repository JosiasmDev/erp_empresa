from django.shortcuts import render, redirect, get_object_or_404
from .models import MovimientoStock
from .forms import MovimientoStockForm
from django.contrib import messages

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