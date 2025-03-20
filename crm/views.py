from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm
from ecommerce.models import Pedido

@role_required(['crm'])
def crm_clientes(request):
    from crm.models import Cliente
    clientes = Cliente.objects.all()
    return render(request, 'crm/clientes.html', {'clientes': clientes})

def is_gerencia_or_admin(user):
    return user.groups.filter(name__in=['Gerencia', 'Administrador']).exists()

def is_cliente(user):
    return user.groups.filter(name='Cliente').exists()

@login_required
def clientes(request):
    clientes = Cliente.objects.all().prefetch_related('pedido_set')
    return render(request, 'crm/clientes.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado.')
            return redirect('crm:clientes')
    else:
        form = ClienteForm()
    context = {
        'form': form,
        'is_gerencia_or_admin': is_gerencia_or_admin(request.user),
        'is_cliente': is_cliente(request.user),
    }
    return render(request, 'crm/crear_cliente.html', context)

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.save()
        return redirect('crm:clientes')
    return render(request, 'crm/editar_cliente.html', {'cliente': cliente})
