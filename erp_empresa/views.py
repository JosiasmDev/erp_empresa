from django.shortcuts import render, get_object_or_404
from ecommerce.models import Coche

def home(request):
    # Filtra los coches Eclipse y Arrow
    coches = Coche.objects.filter(nombre__in=['Eclipse', 'Arrow'])
    context = {'coches': coches}
    return render(request, 'home.html', context)

def index(request):
    return render(request, 'website/index.html')

def contacto(request):
    return render(request, 'website/contacto.html')

def coche_list(request):
    coches = Coche.objects.all()
    return render(request, 'website/coche_list.html', {'coches': coches})

def coche_detalle(request, coche_id):
    coche = get_object_or_404(Coche, pk=coche_id)
    return render(request, 'website/coche_detalle.html', {'coche': coche})