import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

def test_migration():
    print("Creando migración de prueba...")
    try:
        # Crear una migración para una aplicación específica
        execute_from_command_line(['manage.py', 'makemigrations', 'website'])
        
        # Verificar el archivo de migración creado
        migrations_dir = os.path.join('website', 'migrations')
        if os.path.exists(migrations_dir):
            for file in os.listdir(migrations_dir):
                if file.endswith('.py') and file != '__init__.py':
                    file_path = os.path.join(migrations_dir, file)
                    print(f"\nVerificando archivo: {file_path}")
                    try:
                        with open(file_path, 'rb') as f:
                            content = f.read()
                            print(f"Tamaño del archivo: {len(content)} bytes")
                            print(f"Contiene bytes nulos: {b'\x00' in content}")
                            print(f"Primeros 100 bytes: {content[:100]}")
                    except Exception as e:
                        print(f"Error al leer el archivo: {str(e)}")
    except Exception as e:
        print(f"Error durante el proceso: {str(e)}")

if __name__ == '__main__':
    test_migration() 