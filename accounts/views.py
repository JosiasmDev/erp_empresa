from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.username}!')
                return redirect('home')  # Redirige a la página de inicio
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, '¡Registro exitoso! Bienvenido.')
                return redirect('home')  # Redirige a la página de inicio
    else:
        login_form = AuthenticationForm()
        register_form = UserCreationForm()
    
    return render(request, 'accounts/login_register.html', {
        'login_form': login_form,
        'register_form': register_form,
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión.')
    return redirect('home')  # Redirige a la página de inicio

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(is_admin)
def create_employee(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if not username or not password or not role:
            messages.error(request, 'Todos los campos son obligatorios.')
        else:
            try:
                user = User.objects.create_user(username=username, password=password)
                group = Group.objects.get(name=role)
                user.groups.add(group)
                messages.success(request, f'Usuario {username} creado con éxito.')
                return redirect('create_employee')  # Redirige a la misma página después de crear el usuario
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')

    roles = Group.objects.all()
    return render(request, 'accounts/create_employee.html', {'roles': roles})