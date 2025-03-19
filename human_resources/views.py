from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Empleado
from .forms import EmpleadoForm
from django.contrib import messages
from accounts.decorators import role_required

@role_required(['human_resources'])
def hr_empleados(request):
    from human_resources.models import Empleado
    empleados = Empleado.objects.all()
    return render(request, 'human_resources/empleados.html', {'empleados': empleados})

@login_required
def empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'human_resources/empleados.html', {'empleados': empleados})

@login_required
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado.')
            return redirect('human_resources:empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'human_resources/crear_empleado.html', {'form': form})

@login_required
def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado correctamente')
            return redirect('human_resources:empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'human_resources/editar_empleado.html', {'form': form})

@login_required
def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado correctamente')
        return redirect('human_resources:empleados')
    return render(request, 'human_resources/eliminar_empleado.html', {'empleado': empleado})