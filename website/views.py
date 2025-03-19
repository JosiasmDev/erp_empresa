# website/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from ecommerce.models import Coche, Pedido
from accounts.decorators import role_required
from decimal import Decimal
from accounts.models import Profile
from core.models import RelojSimulacion
from django.utils import timezone
from django.contrib import messages

# Formulario dinámico para la personalización del coche
class PersonalizarCocheForm(forms.Form):
    rueda = forms.ChoiceField(choices=Coche.rueda.field.choices, label="Ruedas")
    motorizacion = forms.ChoiceField(choices=Coche.motorizacion.field.choices, label="Motorización")
    tapiceria = forms.ChoiceField(choices=Coche.tapiceria.field.choices, label="Tapicería")
    extras = forms.ChoiceField(choices=Coche.extras.field.choices, label="Extras")

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
    # Inicializar el reloj si no existe
    reloj, created = RelojSimulacion.objects.get_or_create(
        defaults={'fecha_actual': timezone.now(), 'activo': True}
    )
    
    coches = Coche.objects.filter(nombre__in=['Eclipse', 'Arrow'])
    context = {
        'coches': coches,
        'reloj': reloj
    }
    add_user_groups_to_context(request, context)
    return render(request, 'website/index.html', context)

@role_required(['website'])
def contacto(request):
    context = {}
    add_user_groups_to_context(request, context)
    return render(request, 'website/contacto.html', context)

@role_required(['website'])
def coche_list(request):
    coches = Coche.objects.all()
    context = {'coches': coches}
    add_user_groups_to_context(request, context)
    return render(request, 'website/coche_list.html', context)

@login_required
def coche_detalle(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    model_filename = f"{coche.nombre.lower()}.glb"

    # Precios adicionales para cada opción
    precios = {
        'rueda': {'17"': 0, '19"': 1000, '21"': 2000},
        'motorizacion': {'V6 3.0L': 0, 'V8 4.0L': 5000, 'Eléctrico 400kW': 7000},
        'tapiceria': {'Cuero Negro': 0, 'Alcantara Roja': 1500, 'Tela Gris': 500},
        'extras': {'Ninguno': 0, 'Techo Panorámico': 2000, 'Sistema de Sonido Premium': 1500, 'Asistente de Conducción': 3000},
    }

    if request.method == 'POST':
        personalizar_form = PersonalizarCocheForm(request.POST)
        if personalizar_form.is_valid():
            rueda = personalizar_form.cleaned_data['rueda']
            motorizacion = personalizar_form.cleaned_data['motorizacion']
            tapiceria = personalizar_form.cleaned_data['tapiceria']
            extras = personalizar_form.cleaned_data['extras']

            rueda_precio = float(precios['rueda'][rueda])
            motorizacion_precio = float(precios['motorizacion'][motorizacion])
            tapiceria_precio = float(precios['tapiceria'][tapiceria])
            extras_precio = float(precios['extras'][extras])
            precio_total = float(coche.precio_base) + rueda_precio + motorizacion_precio + tapiceria_precio + extras_precio

            # Guardar las selecciones y precios en la sesión
            request.session['rueda'] = rueda
            request.session['motorizacion'] = motorizacion
            request.session['tapiceria'] = tapiceria
            request.session['extras'] = extras
            request.session['rueda_precio'] = rueda_precio
            request.session['motorizacion_precio'] = motorizacion_precio
            request.session['tapiceria_precio'] = tapiceria_precio
            request.session['extras_precio'] = extras_precio
            request.session['precio_total'] = precio_total

            context = {
                'coche': coche,
                'model_filename': model_filename,
                'personalizar_form': personalizar_form,
                'precio_total': precio_total,
                'rueda_precio': rueda_precio,
                'motorizacion_precio': motorizacion_precio,
                'tapiceria_precio': tapiceria_precio,
                'extras_precio': extras_precio,
            }
            add_user_groups_to_context(request, context)
            return redirect('ecommerce:pasarela_pago', coche_id=coche.id)
    else:
        personalizar_form = PersonalizarCocheForm(initial={
            'rueda': coche.rueda,
            'motorizacion': coche.motorizacion,
            'tapiceria': coche.tapiceria,
            'extras': coche.extras,
        })

    rueda_precio = float(precios['rueda'][coche.rueda])
    motorizacion_precio = float(precios['motorizacion'][coche.motorizacion])
    tapiceria_precio = float(precios['tapiceria'][coche.tapiceria])
    extras_precio = float(precios['extras'][coche.extras])
    precio_total = float(coche.precio_base) + rueda_precio + motorizacion_precio + tapiceria_precio + extras_precio

    context = {
        'coche': coche,
        'model_filename': model_filename,
        'personalizar_form': personalizar_form,
        'precio_total': precio_total,
        'rueda_precio': rueda_precio,
        'motorizacion_precio': motorizacion_precio,
        'tapiceria_precio': tapiceria_precio,
        'extras_precio': extras_precio,
    }
    add_user_groups_to_context(request, context)
    return render(request, 'website/coche_detalle.html', context)

@login_required
def perfil_usuario(request):
    # Obtener pedidos del usuario
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha_pedido')
    
    # Obtener perfil del usuario
    try:
        perfil = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        perfil = None
    
    context = {
        'pedidos': pedidos,
        'perfil': perfil,
        'usuario': request.user,
    }
    return render(request, 'website/perfil_usuario.html', context)

@login_required
def arrow_config(request):
    return render(request, 'website/arrow_config.html')

@login_required
def eclipse_config(request):
    return render(request, 'website/eclipse_config.html')