from django.shortcuts import render
from .models import Pagina

def index(request):
    paginas = Pagina.objects.all()
    return render(request, 'website/index.html', {'paginas': paginas})