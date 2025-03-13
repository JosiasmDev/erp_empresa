# website/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Coche
from purchase.forms import CompraForm
from accounts.decorators import role_required

@role_required(['website'])
def home(request):
    return render(request, 'website/index.html')

@role_required(['website'])
def contacto(request):
    return render(request, 'website/contacto.html')

@role_required(['website'])
def coche_detalle(request):
    return render(request, 'website/coche_detalle.html')

def add_user_groups_to_context(request, context):
    """Función auxiliar para agregar variables de grupos al contexto"""
    if request.user.is_authenticated:
        context.update({
            'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
            'is_cliente': request.user.groups.filter(name='Clientes').exists(),
            'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
            'is_compras': request.user.groups.filter(name='Compras').exists(),
            'is_logistica': request.user.groups.filter(name='Logistica').exists(),
        })
    return context

def index(request):
    coches = Coche.objects.filter(nombre__in=['Eclipse', 'Arrow'])
    context = {'coches': coches}
    add_user_groups_to_context(request, context)
    return render(request, 'website/index.html', context)


@role_required(['website'])
def coche_detalle(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    model_filename = f"{coche.nombre.lower()}.glb"
    context = {'coche': coche, 'model_filename': model_filename}
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.coche = coche
            compra.precio_total = float(request.POST.get('precio_total', coche.precio_base))
            compra.save()
            return redirect('purchase_process_payment', compra.id)
    else:
        form = CompraForm(initial={'coche': coche, 'precio_total': coche.precio_base})
    context['form'] = form
    add_user_groups_to_context(request, context)
    return render(request, 'website/coche_detalle.html', context)

@role_required(['website'])
def contacto(request):
    context = {}
    add_user_groups_to_context(request, context)
    return render(request, 'website/contacto.html', context)

def home(request):
    coches = Coche.objects.filter(nombre__in=['Eclipse', 'Arrow'])
    context = {'coches': coches}
    add_user_groups_to_context(request, context)
    return render(request, 'home.html', context)

@role_required(['website'])
def coche_list(request):
    coches = Coche.objects.all()
    return render(request, 'website/coche_list.html', {'coches': coches})