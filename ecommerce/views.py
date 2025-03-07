from django.shortcuts import render, redirect, get_object_or_404
from .models import Coche
from .forms import CocheConfigForm
from django.contrib import messages

def tienda(request):
    coches = Coche.objects.all()
    return render(request, 'ecommerce/tienda.html', {'coches': coches})

def crear_coche(request):
    if request.method == 'POST':
        form = CocheConfigForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coche creado.')
            return redirect('ecommerce_tienda')
    else:
        form = CocheConfigForm()
    return render(request, 'ecommerce/crear_coche.html', {'form': form})