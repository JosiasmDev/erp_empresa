import os
import subprocess
import sys
import shutil
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Directorio raíz donde se ejecutará el script
root_dir = os.getcwd()

# Crear la base de datos en PostgreSQL
try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='aaaaaa',
        host='localhost'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Intentar eliminar la base de datos si existe
    cur.execute("DROP DATABASE IF EXISTS erp_empresa")

    # Crear la base de datos
    cur.execute("CREATE DATABASE erp_empresa")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error al crear la base de datos: {e}")

# 1. Eliminar archivos 0*.py en todas las carpetas migrations
for dirpath, dirnames, filenames in os.walk(root_dir):
    if "migrations" in dirnames:
        migrations_path = os.path.join(dirpath, "migrations")
        for filename in os.listdir(migrations_path):
            if filename.startswith("0") and filename.endswith(".py"):
                os.remove(os.path.join(migrations_path, filename))

# 2. Eliminar carpetas __pycache__ en todas las carpetas migrations
for dirpath, dirnames, filenames in os.walk(root_dir):
    if "migrations" in dirnames:
        migrations_path = os.path.join(dirpath, "migrations")
        pycache_path = os.path.join(migrations_path, "__pycache__")
        if os.path.exists(pycache_path):
            shutil.rmtree(pycache_path)

# 3. Crear directorios management\commands en cada subcarpeta
for subdir in os.listdir(root_dir):
    if os.path.isdir(subdir):
        commands_path = os.path.join(subdir, "management", "commands")
        os.makedirs(commands_path, exist_ok=True)

# 4. Crear __init__.py en cada management
for dirpath, dirnames, filenames in os.walk(root_dir):
    if "management" in dirnames:
        management_path = os.path.join(dirpath, "management")
        open(os.path.join(management_path, "__init__.py"), "a").close()

# 5. Crear __init__.py en cada management\commands
for dirpath, dirnames, filenames in os.walk(root_dir):
    if "commands" in dirnames and "management" in dirpath.split(os.sep):
        commands_path = os.path.join(dirpath, "commands")
        open(os.path.join(commands_path, "__init__.py"), "a").close()

# 6. Ejecutar scripts de Python y comandos de Django
commands = [
    "python manage.py makemigrations",
    "python manage.py migrate",
    "python manage.py loaddata usuarios",
    "python manage.py loaddata coches",
    # Cargamos solo los datos que no dependen de otros modelos
    "python manage.py loaddata datos_iniciales --exclude manufacturing.componente --exclude inventory.componente --exclude inventory.stock --exclude accounting.cuenta --exclude accounting.factura --exclude purchase.ordencompra --exclude purchase.detalleordencompra --exclude manufacturing.ordenfabricacion --exclude manufacturing.componenteorden --exclude human_resources.empleado --exclude human_resources.sueldo --exclude marketing_automation.campana --exclude core.employee --exclude core.inventory --exclude core.productionorder --exclude core.purchaseorder --exclude core.relojsimulacion --exclude website.personalizacioncomponente --exclude website.pagina --exclude sales.pedido --exclude sales.pedidoitem --exclude crm.cliente",
    # Crear superusuario con email
    'echo Josias | python manage.py createsuperuser --username Josias --email josias@example.com --noinput',
    # Establecer contraseña
    'echo aaaaaa | python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username=\'Josias\'); user.set_password(\'aaaaaa\'); user.save()"',
    # Crear datos iniciales
    "python create_initial_data.py",
    "python manage.py runserver"
]

for cmd in commands:
    subprocess.run(cmd, shell=True)