from django.shortcuts import render, redirect, get_object_or_404
from .models import Campana
from .forms import CampanaForm
from django.contrib import messages

def campanas(request):
    campanas = Campana.objects.all()
    return render(request, 'marketing_automation/campanas.html', {'campanas': campanas})

def crear_campana(request):
    if request.method == 'POST':
        form = CampanaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaña creada.')
            return redirect('marketing_campanas')
    else:
        form = CampanaForm()
    return render(request, 'marketing_automation/crear_campana.html', {'form': form})