from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from django.contrib import messages

def tienda(request):
    productos = Producto.objects.all()
    return render(request, 'ecommerce/tienda.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado.')
            return redirect('ecommerce_tienda')
    else:
        form = ProductoForm()
    return render(request, 'ecommerce/crear_producto.html', {'form': form})