from django.shortcuts import render
from .models import Pedido

def pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'sales/pedidos.html', {'pedidos': pedidos})