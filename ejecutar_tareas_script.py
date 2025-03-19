import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

# Importar y ejecutar las tareas
from core.tasks import ejecutar_tareas_programadas

if __name__ == '__main__':
    print('Iniciando ejecución de tareas programadas...')
    ejecutar_tareas_programadas()
    print('Tareas programadas ejecutadas correctamente') 