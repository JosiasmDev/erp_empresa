from django.shortcuts import render
from .models import MovimientoStock

def stock(request):
    movimientos = MovimientoStock.objects.all()
    return render(request, 'inventory/stock.html', {'movimientos': movimientos})