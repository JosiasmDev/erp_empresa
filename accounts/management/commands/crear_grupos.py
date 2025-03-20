from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class Command(BaseCommand):
    help = 'Crea los grupos y asigna los permisos necesarios para cada módulo'

    def handle(self, *args, **kwargs):
        # Lista de grupos y sus permisos
        grupos = {
            'Website': {
                'website': ['view', 'add', 'change', 'delete'],
            },
            'Ventas': {
                'sales': ['view', 'add', 'change', 'delete'],
                'ecommerce': ['view', 'add', 'change', 'delete'],
            },
            'CRM': {
                'crm': ['view', 'add', 'change', 'delete'],
            },
            'Compras': {
                'purchase': ['view', 'add', 'change', 'delete'],
            },
            'Producción': {
                'manufacturing': ['view', 'add', 'change', 'delete'],
            },
            'Inventario': {
                'inventory': ['view', 'add', 'change', 'delete'],
            },
            'RRHH': {
                'human_resources': ['view', 'add', 'change', 'delete'],
            },
            'Marketing': {
                'marketing_automation': ['view', 'add', 'change', 'delete'],
            },
            'Contabilidad': {
                'accounting': ['view', 'add', 'change', 'delete'],
            },
            'Clientes': {
                'website': ['view'],
                'ecommerce': ['view', 'add'],
                'crm': ['view'],
            },
        }

        for grupo_nombre, apps_permisos in grupos.items():
            # Crear o obtener el grupo
            grupo, created = Group.objects.get_or_create(name=grupo_nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{grupo_nombre}" creado exitosamente'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{grupo_nombre}" ya existe'))

            # Asignar permisos para cada app
            for app_name, permisos in apps_permisos.items():
                try:
                    app_config = apps.get_app_config(app_name)
                    for modelo in app_config.get_models():
                        content_type = ContentType.objects.get_for_model(modelo)
                        for permiso in permisos:
                            codename = f'{permiso}_{modelo._meta.model_name}'
                            try:
                                permiso_obj = Permission.objects.get(content_type=content_type, codename=codename)
                                grupo.permissions.add(permiso_obj)
                                self.stdout.write(self.style.SUCCESS(
                                    f'Permiso "{codename}" asignado al grupo "{grupo_nombre}"'
                                ))
                            except Permission.DoesNotExist:
                                self.stdout.write(self.style.WARNING(
                                    f'Permiso "{codename}" no encontrado para el modelo {modelo._meta.model_name}'
                                ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error al procesar la app "{app_name}": {str(e)}'
                    ))

        self.stdout.write(self.style.SUCCESS('Proceso completado'))