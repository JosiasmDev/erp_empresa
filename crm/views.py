from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'crm/clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado.')
            return redirect('crm_clientes')
    else:
        form = ClienteForm()
    return render(request, 'crm/crear_cliente.html', {'form': form})