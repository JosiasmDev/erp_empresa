from django.shortcuts import render, redirect, get_object_or_404
from .models import Compra
from .forms import CompraForm
from django.contrib import messages

def compras(request):
    compras = Compra.objects.all()
    return render(request, 'purchase/compras.html', {'compras': compras})

def crear_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compra creada.')
            return redirect('purchase_compras')
    else:
        form = CompraForm()
    return render(request, 'purchase/crear_compra.html', {'form': form})