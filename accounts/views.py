from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from accounting.models import Cuenta
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from sales.models import Pedido
from inventory.models import OrdenEntrega

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
                return redirect(request.GET.get('next', '/'))
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, '¡Registro exitoso! Bienvenido.')
                return redirect(request.GET.get('next', '/'))
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
    return redirect('/')

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
    cuentas = Cuenta.objects.all()
    context = {
        'cuentas': cuentas,
        **get_user_roles(request.user)
    }
    return render(request, 'accounting/facturas.html', context)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance, role='administrador')

@login_required
def perfil(request):
    # Obtener los pedidos entregados del cliente
    pedidos_entregados = []
    if request.user.groups.filter(name='Clientes').exists():
        pedidos_entregados = Pedido.objects.filter(
            cliente__user=request.user,
            estado='entregado'
        ).select_related('coche')
    
    context = {
        'pedidos_entregados': pedidos_entregados,
        **get_user_roles(request.user)
    }
    return render(request, 'accounts/perfil.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.username}!')
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {
        'form': form,
        'error': form.errors.get('__all__') if request.method == 'POST' else None
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Asignar el grupo de Cliente por defecto
            cliente_group = Group.objects.get_or_create(name='Clientes')[0]
            user.groups.add(cliente_group)
            # Crear el perfil del usuario solo si no existe
            Profile.objects.get_or_create(user=user, defaults={'role': 'cliente'})
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a nuestra plataforma.')
            return redirect('website:index')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})