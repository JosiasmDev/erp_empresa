from django.shortcuts import render
from .models import Compra

def compras(request):
    compras = Compra.objects.all()
    return render(request, 'purchase/compras.html', {'compras': compras})