from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from accounting.models import Factura
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

def get_user_roles(user):
    return {
        'roles': [group.name for group in user.groups.all()]
    }

def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.username}!')
                return redirect(request.GET.get('next', 'home'))
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, '¡Registro exitoso! Bienvenido.')
                return redirect(request.GET.get('next', 'home'))
            else:
                messages.error(request, 'Error al registrarse. Verifica los datos.')
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
    return redirect('home')

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
                role_mapping = {
                    'Administrador': 'administrador',
                    'Gerente': 'gerente',
                    'Finanzas': 'finanzas',
                    'Producción': 'produccion',
                    'Recursos Humanos': 'recursos_humanos',
                    'Marketing': 'marketing',
                    'Cliente': 'cliente',  # Nuevo mapeo para el rol Cliente
                }
                Profile.objects.create(user=user, role=role_mapping.get(role, 'administrador'))
                messages.success(request, f'Usuario {username} creado con éxito.')
                return redirect('create_employee')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')

    roles = Group.objects.all()
    return render(request, 'accounts/create_employee.html', {'roles': roles})

@login_required
def facturas_view(request):
    facturas = Factura.objects.all()
    context = {
        'facturas': facturas,
        **get_user_roles(request.user)
    }
    return render(request, 'accounting/facturas.html', context)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance, role='administrador')