from django.shortcuts import render
from .models import Campana

def campanas(request):
    campanas = Campana.objects.all()
    return render(request, 'marketing_automation/campanas.html', {'campanas': campanas})