from django.shortcuts import render, redirect, get_object_or_404
from .models import Campana
from .forms import CampanaForm
from django.contrib import messages
from accounts.decorators import role_required

@role_required(['marketing_automation'])
def marketing_automation_campanas(request):
    from marketing_automation.models import Campana
    campanas = Campana.objects.all()
    return render(request, 'marketing_automation/campanas.html', {'campanas': campanas})

def campanas(request):
    campanas = Campana.objects.all()
    return render(request, 'marketing_automation/campanas.html', {'campanas': campanas})

def crear_campana(request):
    if request.method == 'POST':
        form = CampanaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaña creada.')
            return redirect('marketing_automation_campanas')  # Cambiado de 'marketing_campanas'
    else:
        form = CampanaForm()
    return render(request, 'marketing_automation/crear_campana.html', {'form': form})