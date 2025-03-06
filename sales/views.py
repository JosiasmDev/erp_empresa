from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido, PedidoItem
from .forms import PedidoForm, PedidoItemForm
from django.contrib import messages

def pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'sales/pedidos.html', {'pedidos': pedidos})

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('sales_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'sales/crear_pedido.html', {'form': form})

def agregar_item(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        form = PedidoItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido
            item.save()
            messages.success(request, 'Ítem añadido.')
            return redirect('sales_pedidos')
    else:
        form = PedidoItemForm()
    return render(request, 'sales/agregar_item.html', {'form': form, 'pedido': pedido})