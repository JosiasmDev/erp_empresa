from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado
from .forms import EmpleadoForm
from django.contrib import messages

def empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'human_resources/empleados.html', {'empleados': empleados})

def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado.')
            return redirect('hr_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'human_resources/crear_empleado.html', {'form': form})