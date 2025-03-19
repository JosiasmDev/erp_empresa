from django.core.management.base import BaseCommand
from core.tasks import ejecutar_tareas_programadas

class Command(BaseCommand):
    help = 'Ejecuta las tareas programadas del sistema'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando ejecución de tareas programadas...')
        ejecutar_tareas_programadas()
        self.stdout.write(self.style.SUCCESS('Tareas programadas ejecutadas correctamente')) 