from django.shortcuts import render
from .models import Empleado

def empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'human_resources/empleados.html', {'empleados': empleados})