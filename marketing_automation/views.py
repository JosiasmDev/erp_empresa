from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from .models import Campana
from .forms import CampanaForm, CocheForm, PersonalizacionComponenteForm
from website.models import Coche, PersonalizacionComponente

@role_required(['marketing'])
def campanas(request):
    campanas = Campana.objects.all()
    return render(request, 'marketing_automation/campanas.html', {'campanas': campanas})

@role_required(['marketing'])
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

@role_required(['marketing'])
def lista_coches(request):
    coches = Coche.objects.all()
    return render(request, 'marketing_automation/lista_coches.html', {'coches': coches})

@role_required(['marketing'])
def editar_coche(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    componentes = coche.componentes.all()

    if request.method == 'POST':
        coche_form = CocheForm(request.POST, instance=coche)
        if coche_form.is_valid():
            coche_form.save()
            for componente in componentes:
                comp_form = PersonalizacionComponenteForm(request.POST, prefix=f'comp_{componente.id}', instance=componente)
                if comp_form.is_valid():
                    comp_form.save()
            messages.success(request, 'Coche y componentes actualizados.')
            return redirect('marketing_automation:lista_coches')
    else:
        coche_form = CocheForm(instance=coche)
        componente_forms = [PersonalizacionComponenteForm(instance=comp, prefix=f'comp_{comp.id}') for comp in componentes]

    return render(request, 'marketing_automation/editar_coche.html', {
        'coche_form': coche_form,
        'componente_forms': componente_forms,
        'coche': coche,
    })

@role_required(['marketing', 'administrador', 'gerente'])
def editar_todos_coches(request):
    coches = Coche.objects.all()

    if request.method == 'POST':
        for coche in coches:
            coche_form = CocheForm(request.POST, prefix=f'coche_{coche.id}', instance=coche)
            if coche_form.is_valid():
                coche_form.save()
            componentes = coche.componentes.all()
            for componente in componentes:
                comp_form = PersonalizacionComponenteForm(request.POST, prefix=f'comp_{coche.id}_{componente.id}', instance=componente)
                if comp_form.is_valid():
                    comp_form.save()
        messages.success(request, 'Todos los coches y componentes actualizados.')
        return redirect('marketing_automation:editar_todos_coches')
    else:
        coche_forms = [CocheForm(instance=coche, prefix=f'coche_{coche.id}') for coche in coches]
        all_componente_forms = []
        for coche in coches:
            componente_forms = [PersonalizacionComponenteForm(instance=comp, prefix=f'comp_{coche.id}_{comp.id}') for comp in coche.componentes.all()]
            all_componente_forms.extend(componente_forms)

    return render(request, 'marketing_automation/editar_todos_coches.html', {
        'coche_forms': coche_forms,
        'componente_forms': all_componente_forms,
    })