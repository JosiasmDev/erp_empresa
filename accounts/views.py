from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

def login_register(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.username}!')
                return redirect('/')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                user.groups.add(Group.objects.get(name='Clientes'))
                login(request, user)
                messages.success(request, '¡Registro exitoso! Bienvenido.')
                return redirect('/')
            else:
                messages.error(request, 'Error en el registro. Verifica los datos.')
    
    return render(request, 'accounts/login_register.html', {
        'login_form': login_form,
        'register_form': register_form,
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión.')
    return redirect('/')

@login_required
@user_passes_test(is_admin)
def create_employee(request):
    roles = ['Clientes', 'RRHH', 'Compras', 'Logistica', 'Gerencia', 'Administrador']  # Lista de roles permitidos
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')  # Email es opcional
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Validar que todos los campos necesarios estén presentes
        if not username or not password or not role:
            messages.error(request, 'Por favor, completa todos los campos requeridos.')
        elif role not in roles:
            messages.error(request, 'Rol no válido.')
        else:
            try:
                # Crear el usuario
                user = User.objects.create_user(username=username, email=email, password=password)
                # Asignar el rol
                user.groups.add(Group.objects.get(name=role))
                messages.success(request, f'Usuario {username} creado exitosamente.')
                return redirect('/')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')

    return render(request, 'accounts/create_employee.html', {'roles': roles})