from django.shortcuts import render
from ecommerce.models import Coche

def home(request):
    # Filtra los coches Eclipse y Arrow
    coches = Coche.objects.filter(nombre__in=['Eclipse', 'Arrow'])
    context = {'coches': coches}
    return render(request, 'home.html', context)