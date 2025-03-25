from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Carga los datos iniciales en la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cargando datos iniciales...')
        call_command('loaddata', 'coches.json', verbosity=0)
        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados exitosamente')) 