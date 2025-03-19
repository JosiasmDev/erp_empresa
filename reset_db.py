import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

def reset_database():
    print("Iniciando proceso de reinicio de la base de datos...")
    
    # Eliminar todas las migraciones
    print("Eliminando migraciones...")
    for app in ['website', 'ecommerce', 'manufacturing', 'inventory', 'sales', 'purchase', 'accounting', 'crm', 'human_resources', 'marketing_automation']:
        migrations_dir = os.path.join(app, 'migrations')
        if os.path.exists(migrations_dir):
            for file in os.listdir(migrations_dir):
                if file.endswith('.py') and file != '__init__.py':
                    os.remove(os.path.join(migrations_dir, file))
    
    # Eliminar archivos __pycache__
    print("Eliminando archivos __pycache__...")
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            for file in os.listdir(cache_dir):
                os.remove(os.path.join(cache_dir, file))
            os.rmdir(cache_dir)
    
    # Crear nuevas migraciones
    print("Creando nuevas migraciones...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Aplicar migraciones
    print("Aplicando migraciones...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Cargar datos iniciales
    print("Cargando datos iniciales...")
    execute_from_command_line(['manage.py', 'loaddata', 'usuarios.json'])
    execute_from_command_line(['manage.py', 'loaddata', 'datos_iniciales.json'])
    
    print("¡Proceso completado exitosamente!")
    print("\nUsuarios creados:")
    print("1. Administrador:")
    print("   Usuario: admin")
    print("   Contraseña: aaaaaa")
    print("\n2. Cliente de ejemplo:")
    print("   Usuario: cliente1")
    print("   Contraseña: aaaaaa")

if __name__ == '__main__':
    reset_database() 