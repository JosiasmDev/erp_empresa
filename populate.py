import os
import django

# Establecer la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.db import IntegrityError

# Crear grupos (si no existen)
def create_groups():
    groups = ['Clientes', 'RRHH', 'Compras', 'Logistica', 'Gerencia', 'Administrador']
    for group_name in groups:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Grupo '{group_name}' creado.")
        else:
            print(f"Grupo '{group_name}' ya existe.")

# Crear superusuario
def create_superuser():
    try:
        superuser = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        print("Superusuario creado con éxito.")
    except IntegrityError:
        print("El superusuario ya existe.")

# Crear usuario de ejemplo
def create_example_users():
    example_users = [
        {'username': 'johndoe', 'email': 'johndoe@example.com', 'password': '1234'},
        {'username': 'janedoe', 'email': 'janedoe@example.com', 'password': '1234'}
    ]
    
    for user_data in example_users:
        try:
            user = User.objects.create_user(
                username=user_data['username'], 
                email=user_data['email'], 
                password=user_data['password']
            )
            print(f"Usuario '{user.username}' creado.")
        except IntegrityError:
            print(f"El usuario '{user_data['username']}' ya existe.")

# Función principal para poblar la base de datos
def populate_database():
    create_groups()  # Crear grupos
    create_superuser()  # Crear superusuario
    create_example_users()  # Crear usuarios de ejemplo

if __name__ == "__main__":
    populate_database()
