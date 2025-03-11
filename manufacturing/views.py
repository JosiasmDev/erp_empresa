from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdenProduccion
from .forms import OrdenProduccionForm
from django.contrib import messages
from django.core.paginator import Paginator

def produccion(request):
    ordenes_list = OrdenProduccion.objects.all()
    paginator = Paginator(ordenes_list, 10)  # Muestra 10 órdenes por página
    page_number = request.GET.get('page')
    ordenes = paginator.get_page(page_number)
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