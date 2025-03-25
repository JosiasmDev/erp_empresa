from django.core.management.base import BaseCommand
from manufacturing.models import Componente

class Command(BaseCommand):
    help = 'Crea los componentes iniciales necesarios para la fabricación de vehículos'

    def handle(self, *args, **kwargs):
        componentes = [
            {
                'nombre': 'Ruedas',
                'descripcion': 'Juego de ruedas para el vehículo',
                'stock_minimo': 10,
                'precio_compra': 1000.00,
            },
            {
                'nombre': 'Motorizacion',
                'descripcion': 'Motor y componentes relacionados',
                'stock_minimo': 5,
                'precio_compra': 5000.00,
            },
            {
                'nombre': 'Tapiceria',
                'descripcion': 'Tapicería completa del vehículo',
                'stock_minimo': 8,
                'precio_compra': 2000.00,
            },
            {
                'nombre': 'Extras',
                'descripcion': 'Componentes adicionales y extras',
                'stock_minimo': 15,
                'precio_compra': 1500.00,
            },
        ]

        for comp_data in componentes:
            Componente.objects.get_or_create(
                nombre=comp_data['nombre'],
                defaults=comp_data
            )
            self.stdout.write(self.style.SUCCESS(f'Componente {comp_data["nombre"]} creado o actualizado')) 