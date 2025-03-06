from django.shortcuts import render
from .models import OrdenProduccion

def produccion(request):
    ordenes = OrdenProduccion.objects.all()
    return render(request, 'manufacturing/produccion.html', {'ordenes': ordenes})