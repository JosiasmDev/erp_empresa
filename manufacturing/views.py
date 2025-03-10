from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdenProduccion
from .forms import OrdenProduccionForm
from django.contrib import messages

def produccion(request):
    ordenes = OrdenProduccion.objects.all()
    return render(request, 'manufacturing/produccion.html', {'ordenes': ordenes})

def crear_orden(request):
    if request.method == 'POST':
        form = OrdenProduccionForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.completada = False  # Inicializar como False
            orden.save()
            messages.success(request, 'Orden creada.')
            return redirect('manufacturing_produccion')
    else:
        form = OrdenProduccionForm()
    return render(request, 'manufacturing/crear_orden.html', {'form': form})