from django.shortcuts import render, redirect, get_object_or_404
from ecommerce.models import Coche
from .forms import CocheConfigForm
from django.contrib import messages

def index(request):
    coches = Coche.objects.all()
    return render(request, 'website/index.html', {'coches': coches})

def coche_detalle(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    # Generar el nombre del archivo del modelo 3D
    model_filename = coche.nombre.lower() + ".glb"
    if request.method == 'POST':
        form = CocheConfigForm(request.POST, instance=coche)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración actualizada.')
            return redirect('website_coche_detalle', coche_id=coche.id)
    else:
        form = CocheConfigForm(instance=coche)
    return render(request, 'website/coche_detalle.html', {'coche': coche, 'form': form, 'model_filename': model_filename})