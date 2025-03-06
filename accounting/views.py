from django.shortcuts import render, redirect, get_object_or_404
from .models import Factura
from .forms import FacturaForm
from django.contrib import messages

def facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'accounting/facturas.html', {'facturas': facturas})

def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Factura creada.')
            return redirect('accounting_facturas')
    else:
        form = FacturaForm()
    return render(request, 'accounting/crear_factura.html', {'form': form})