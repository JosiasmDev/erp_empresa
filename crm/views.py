from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages
from accounts.decorators import role_required

@role_required(['crm'])
def crm_clientes(request):
    from crm.models import Cliente
    clientes = Cliente.objects.all()
    return render(request, 'crm/clientes.html', {'clientes': clientes})

def is_gerencia_or_admin(user):
    return user.groups.filter(name__in=['Gerencia', 'Administrador']).exists()

def is_cliente(user):
    return user.groups.filter(name='Cliente').exists()

def clientes(request):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes,
        'is_gerencia_or_admin': is_gerencia_or_admin(request.user),
        'is_cliente': is_cliente(request.user),
    }
    return render(request, 'crm/clientes.html', context)

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado.')
            return redirect('crm_clientes')
    else:
        form = ClienteForm()
    context = {
        'form': form,
        'is_gerencia_or_admin': is_gerencia_or_admin(request.user),
        'is_cliente': is_cliente(request.user),
    }
    return render(request, 'crm/crear_cliente.html', context)
