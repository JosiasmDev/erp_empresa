from django.shortcuts import render
from .models import Factura

def facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'accounting/facturas.html', {'facturas': facturas})