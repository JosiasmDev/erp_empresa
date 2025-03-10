from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

def login_register(request):
    login_form = AuthenticationForm()  # Inicializar fuera del if
    register_form = UserCreationForm()  # Inicializar fuera del if
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.username}!')
                return redirect('/')
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                # Asignar rol de cliente por defecto
                user.groups.add(Group.objects.get(name='Clientes'))
                login(request, user)
                messages.success(request, '¡Registro exitoso! Bienvenido.')
                return redirect('/')
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
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.groups.add(Group.objects.get(name=role))
        return redirect('/')
    return render(request, 'accounts/create_employee.html', {'roles': ['RRHH', 'Compras', 'Logistica', 'Gerencia']})