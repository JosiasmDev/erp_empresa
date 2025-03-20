import os
import sys
import django
import psycopg2
from django.core.management import execute_from_command_line
import time

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')

def reset_database():
    print("Iniciando proceso de reinicio de la base de datos...")
    
    # Conectar a PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='aaaaaa',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Cerrar todas las conexiones a la base de datos
        print("Cerrando conexiones existentes...")
        cur.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'erp_empresa'
            AND pid <> pg_backend_pid();
        """)
        
        # Eliminar la base de datos si existe
        print("Eliminando base de datos existente...")
        cur.execute("DROP DATABASE IF EXISTS erp_empresa")
        
        # Crear nueva base de datos con la configuración correcta
        print("Creando nueva base de datos...")
        cur.execute("""
            CREATE DATABASE erp_empresa
            WITH
            OWNER = postgres
            ENCODING = 'UTF8'
            LC_COLLATE = 'es-ES'
            LC_CTYPE = 'es-ES'
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1
        """)
        
        # Cerrar conexión
        cur.close()
        conn.close()
        
        # Esperar a que la base de datos esté disponible
        print("Esperando a que la base de datos esté disponible...")
        time.sleep(2)
        
    except Exception as e:
        print(f"Error al resetear la base de datos: {str(e)}")
        sys.exit(1)
    
    # Configurar Django después de crear la base de datos
    django.setup()
    
    # Eliminar todas las migraciones
    print("Eliminando migraciones...")
    for app in ['website', 'ecommerce', 'manufacturing', 'inventory', 'sales', 'purchase', 'accounting', 'crm', 'human_resources', 'marketing_automation', 'accounts', 'core']:
        migrations_dir = os.path.join(app, 'migrations')
        if os.path.exists(migrations_dir):
            for file in os.listdir(migrations_dir):
                if file.endswith('.py') and file != '__init__.py':
                    try:
                        os.remove(os.path.join(migrations_dir, file))
                    except Exception as e:
                        print(f"No se pudo eliminar {file}: {str(e)}")
    
    # Eliminar archivos __pycache__
    print("Eliminando archivos __pycache__...")
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            for file in os.listdir(cache_dir):
                try:
                    os.remove(os.path.join(cache_dir, file))
                except Exception as e:
                    print(f"No se pudo eliminar {file}: {str(e)}")
            try:
                os.rmdir(cache_dir)
            except Exception as e:
                print(f"No se pudo eliminar el directorio {cache_dir}: {str(e)}")
    
    # Crear nuevas migraciones
    print("Creando nuevas migraciones...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Aplicar migraciones
    print("Aplicando migraciones...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Cargar datos del backup
    print("Cargando datos del backup...")
    try:
        execute_from_command_line(['manage.py', 'loaddata', 'backup_db.json'])
    except Exception as e:
        print(f"Error al cargar datos del backup: {str(e)}")
    
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