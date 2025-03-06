from django.shortcuts import render, redirect, get_object_or_404
from .models import Pagina
from .forms import PaginaForm
from django.contrib import messages

def index(request):
    paginas = Pagina.objects.all()
    return render(request, 'website/index.html', {'paginas': paginas})

def crear_pagina(request):
    if request.method == 'POST':
        form = PaginaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Página creada.')
            return redirect('website_index')
    else:
        form = PaginaForm()
    return render(request, 'website/crear_pagina.html', {'form': form})