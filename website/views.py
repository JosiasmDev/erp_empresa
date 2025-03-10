from django.shortcuts import render, get_object_or_404
from .models import Coche
from django.contrib.auth.decorators import login_required
from purchase.forms import CompraForm

def index(request):
    coches = Coche.objects.all()
    context = {'coches': coches}
    if request.user.is_authenticated:
        context.update({
            'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
            'is_cliente': request.user.groups.filter(name='Clientes').exists(),
            'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
            'is_compras': request.user.groups.filter(name='Compras').exists(),
            'is_logistica': request.user.groups.filter(name='Logistica').exists(),
        })
    return render(request, 'website/index.html', context)

def coche_detalle(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    model_filename = f"{coche.nombre.lower()}.glb"
    context = {'coche': coche, 'model_filename': model_filename}
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'website/login_required.html')
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
    if request.user.is_authenticated:
        context.update({
            'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
            'is_cliente': request.user.groups.filter(name='Clientes').exists(),
            'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
            'is_compras': request.user.groups.filter(name='Compras').exists(),
            'is_logistica': request.user.groups.filter(name='Logistica').exists(),
        })
    return render(request, 'website/coche_detalle.html', context)

def contacto(request):
    context = {}
    if request.user.is_authenticated:
        context.update({
            'is_gerencia_or_admin': request.user.groups.filter(name__in=['Gerencia', 'Administrador']).exists() or request.user.is_superuser,
            'is_cliente': request.user.groups.filter(name='Clientes').exists(),
            'is_rrhh': request.user.groups.filter(name='RRHH').exists(),
            'is_compras': request.user.groups.filter(name='Compras').exists(),
            'is_logistica': request.user.groups.filter(name='Logistica').exists(),
        })
    return render(request, 'website/contacto.html', context)