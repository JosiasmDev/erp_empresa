from django.contrib.auth.models import Group
from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'Crea grupos y asigna permisos para el ERP Empresa'

    def handle(self, *args, **kwargs):
        groups_permissions = {
            'Administrador': ['*'],
            'Gerente': ['*'],
            'Finanzas': ['accounting', 'crm', 'sales', 'purchase'],
            'Producción': ['manufacturing', 'inventory'],
            'Recursos Humanos': ['human_resources', 'create_employee'],
            'Marketing': ['marketing_automation', 'ecommerce'],
            'Cliente': ['website', 'home'],
        }

        for group_name, modules in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo {group_name} creado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo {group_name} ya existe.'))

        self.stdout.write(self.style.SUCCESS('Configuración de grupos completada.'))