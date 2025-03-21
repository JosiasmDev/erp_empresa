from django.core.management.base import BaseCommand
from ecommerce.models import Coche
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea coches de ejemplo con precios base'

    def handle(self, *args, **kwargs):
        coches = [
            {
                'nombre': 'Modelo S',
                'precio_base': Decimal('80000.00'),
                'potencia': 500,
                'velocidad_maxima': 250,
                'descripcion': 'Sedán de lujo con alto rendimiento',
                'color': 'Negro',
                'rueda': '19"',
                'motorizacion': 'V6 3.0L',
                'tapiceria': 'Cuero Negro',
                'extras': 'Techo Panorámico'
            },
            {
                'nombre': 'Modelo X',
                'precio_base': Decimal('90000.00'),
                'potencia': 600,
                'velocidad_maxima': 280,
                'descripcion': 'SUV deportivo de alto rendimiento',
                'color': 'Rojo',
                'rueda': '21"',
                'motorizacion': 'V8 4.0L',
                'tapiceria': 'Alcantara Roja',
                'extras': 'Sistema de Sonido Premium'
            },
            {
                'nombre': 'Modelo 3',
                'precio_base': Decimal('45000.00'),
                'potencia': 400,
                'velocidad_maxima': 220,
                'descripcion': 'Sedán compacto eléctrico',
                'color': 'Azul',
                'rueda': '17"',
                'motorizacion': 'Eléctrico 400kW',
                'tapiceria': 'Tela Gris',
                'extras': 'Asistente de Conducción'
            }
        ]

        for coche_data in coches:
            Coche.objects.get_or_create(
                nombre=coche_data['nombre'],
                defaults=coche_data
            )

        self.stdout.write(self.style.SUCCESS('Coches de ejemplo creados exitosamente')) 