from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django import forms
from accounts.decorators import role_required
from .models import Campana
from .forms import CampanaForm, CocheForm
from ecommerce.models import Coche  # Cambia esta importación

# Formulario para editar las opciones de personalización
class CochePersonalizacionForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = ['rueda', 'motorizacion', 'tapiceria', 'extras']

@role_required(['marketing', 'administrador', 'gerente'])
def campanas(request):
    campanas = Campana.objects.all()
    return render(request, 'marketing_automation/campanas.html', {'campanas': campanas})

@role_required(['marketing', 'administrador', 'gerente'])
def crear_campana(request):
    if request.method == 'POST':
        form = CampanaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaña creada.')
            return redirect('marketing_automation:campanas')
    else:
        form = CampanaForm()
    return render(request, 'marketing_automation/crear_campana.html', {'form': form})

@role_required(['marketing', 'administrador', 'gerente'])
def lista_coches(request):
    coches = Coche.objects.all()
    print(f"Coches encontrados: {coches}")
    return render(request, 'marketing_automation/lista_coches.html', {'coches': coches})

@role_required(['marketing', 'administrador', 'gerente'])
def editar_coche(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    if request.method == 'POST':
        coche_form = CocheForm(request.POST, instance=coche)
        personalizacion_form = CochePersonalizacionForm(request.POST, instance=coche)
        if coche_form.is_valid() and personalizacion_form.is_valid():
            coche_form.save()
            personalizacion_form.save()
            messages.success(request, 'Coche actualizado.')
            return redirect('marketing_automation:editar_todos_coches')
    else:
        coche_form = CocheForm(instance=coche)
        personalizacion_form = CochePersonalizacionForm(instance=coche)

    return render(request, 'marketing_automation/editar_coche.html', {
        'coche_form': coche_form,
        'personalizacion_form': personalizacion_form,
        'coche': coche,
    })

@role_required(['marketing', 'administrador', 'gerente'])
def editar_todos_coches(request):
    coches = Coche.objects.all()

    if request.method == 'POST':
        for coche in coches:
            coche_form = CocheForm(request.POST, prefix=f'coche_{coche.id}', instance=coche)
            personalizacion_form = CochePersonalizacionForm(request.POST, prefix=f'personalizar_{coche.id}', instance=coche)
            if coche_form.is_valid() and personalizacion_form.is_valid():
                coche_form.save()
                personalizacion_form.save()
        messages.success(request, 'Todos los coches y componentes actualizados.')
        return redirect('marketing_automation:editar_todos_coches')
    else:
        coche_forms = [(CocheForm(instance=coche, prefix=f'coche_{coche.id}'), CochePersonalizacionForm(instance=coche, prefix=f'personalizar_{coche.id}')) for coche in coches]

    return render(request, 'marketing_automation/editar_todos_coches.html', {
        'coche_forms': coche_forms,
    })