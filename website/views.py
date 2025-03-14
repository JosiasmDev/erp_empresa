# website/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django import forms
from ecommerce.models import Coche  # Cambia esta importación
from purchase.forms import CompraForm
from accounts.decorators import role_required

# Formulario dinámico para la personalización del coche
class PersonalizarCocheForm(forms.Form):
    rueda = forms.ChoiceField(choices=Coche.rueda.field.choices, label="Ruedas")
    motorizacion = forms.ChoiceField(choices=Coche.motorizacion.field.choices, label="Motorización")
    tapiceria = forms.ChoiceField(choices=Coche.tapiceria.field.choices, label="Tapicería")
    extras = forms.ChoiceField(choices=Coche.extras.field.choices, label="Extras")

@role_required(['website'])
def home(request):
    coches = Coche.objects.filter(nombre__in=['Eclipse', 'Arrow'])
    context = {'coches': coches}
    add_user_groups_to_context(request, context)
    return render(request, 'website/index.html', context)

@role_required(['website'])
def contacto(request):
    context = {}
    add_user_groups_to_context(request, context)
    return render(request, 'website/contacto.html', context)

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

    # Precios adicionales para cada opción
    precios = {
        'rueda': {
            '17"': 0,
            '19"': 1000,
            '21"': 2000,
        },
        'motorizacion': {
            'V6 3.0L': 0,
            'V8 4.0L': 5000,
            'Eléctrico 400kW': 7000,
        },
        'tapiceria': {
            'Cuero Negro': 0,
            'Alcantara Roja': 1500,
            'Tela Gris': 500,
        },
        'extras': {
            'Ninguno': 0,
            'Techo Panorámico': 2000,
            'Sistema de Sonido Premium': 1500,
            'Asistente de Conducción': 3000,
        },
    }

    if request.method == 'POST':
        personalizar_form = PersonalizarCocheForm(request.POST)
        compra_form = CompraForm(request.POST)

        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")

        if personalizar_form.is_valid():
            # Calcular el precio total
            precio_base = coche.precio_base
            rueda_precio = precios['rueda'][personalizar_form.cleaned_data['rueda']]
            motorizacion_precio = precios['motorizacion'][personalizar_form.cleaned_data['motorizacion']]
            tapiceria_precio = precios['tapiceria'][personalizar_form.cleaned_data['tapiceria']]
            extras_precio = precios['extras'][personalizar_form.cleaned_data['extras']]
            precio_total = precio_base + rueda_precio + motorizacion_precio + tapiceria_precio + extras_precio

            if compra_form.is_valid():
                compra = compra_form.save(commit=False)
                compra.coche = coche
                compra.precio_total = precio_total
                compra.save()
                return redirect('purchase_process_payment', compra.id)

            context = {
                'coche': coche,
                'model_filename': model_filename,
                'personalizar_form': personalizar_form,
                'compra_form': compra_form,
                'precio_total': precio_total,
                'rueda_precio': rueda_precio,
                'motorizacion_precio': motorizacion_precio,
                'tapiceria_precio': tapiceria_precio,
                'extras_precio': extras_precio,
            }
            add_user_groups_to_context(request, context)
            return render(request, 'website/coche_detalle.html', context)
    else:
        personalizar_form = PersonalizarCocheForm(initial={
            'rueda': coche.rueda,
            'motorizacion': coche.motorizacion,
            'tapiceria': coche.tapiceria,
            'extras': coche.extras,
        })
        compra_form = CompraForm(initial={'coche': coche, 'precio_total': coche.precio_base})

    context = {
        'coche': coche,
        'model_filename': model_filename,
        'personalizar_form': personalizar_form,
        'compra_form': compra_form,
        'precio_total': coche.precio_base,  # Precio inicial sin extras
    }
    add_user_groups_to_context(request, context)
    return render(request, 'website/coche_detalle.html', context)

@role_required(['website'])
def coche_list(request):
    coches = Coche.objects.all()
    return render(request, 'website/coche_list.html', {'coches': coches})