from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import OrdenProduccion
from .forms import OrdenProduccionForm
from accounts.decorators import role_required

@login_required
@role_required(['Produccion'])
def manufacturing_produccion(request):
    ordenes_list = OrdenProduccion.objects.all().order_by('-fecha_inicio')  # Añadimos ordenamiento por fecha_inicio descendente
    paginator = Paginator(ordenes_list, 10)  # Muestra 10 órdenes por página
    page_number = request.GET.get('page')
    ordenes = paginator.get_page(page_number)
    
    context = {
        'ordenes': ordenes,
        'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
        'is_cliente': request.user.groups.filter(name='Clientes').exists(),
        'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
        'is_compras': request.user.groups.filter(name='Compras').exists(),
        'is_logistica': request.user.groups.filter(name='Logistica').exists(),
    }
    return render(request, 'manufacturing/produccion.html', context)

@login_required
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
    context = {
        'form': form,
        'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
        'is_cliente': request.user.groups.filter(name='Clientes').exists(),
        'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
        'is_compras': request.user.groups.filter(name='Compras').exists(),
        'is_logistica': request.user.groups.filter(name='Logistica').exists(),
    }
    return render(request, 'manufacturing/crear_orden.html', context)