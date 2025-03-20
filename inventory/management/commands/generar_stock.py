from django.core.management.base import BaseCommand
from inventory.models import Componente, Stock, MovimientoStock
from decimal import Decimal

class Command(BaseCommand):
    help = 'Genera datos de stock inicial para los componentes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generando datos de stock...')

        # Datos de componentes
        componentes_data = [
            # Ruedas
            {'tipo': 'ruedas_17', 'nombre': 'Ruedas 17"', 'descripcion': 'Ruedas de aleación 17 pulgadas', 'precio_venta': 800.00, 'precio_compra': 400.00},
            {'tipo': 'ruedas_19', 'nombre': 'Ruedas 19"', 'descripcion': 'Ruedas de aleación 19 pulgadas', 'precio_venta': 1000.00, 'precio_compra': 500.00},
            {'tipo': 'ruedas_21', 'nombre': 'Ruedas 21"', 'descripcion': 'Ruedas de aleación 21 pulgadas', 'precio_venta': 1200.00, 'precio_compra': 600.00},
            
            # Motores
            {'tipo': 'motor_v6', 'nombre': 'Motor V6 3.0L', 'descripcion': 'Motor V6 de 3.0 litros', 'precio_venta': 5000.00, 'precio_compra': 2500.00},
            {'tipo': 'motor_v8', 'nombre': 'Motor V8 4.0L', 'descripcion': 'Motor V8 de 4.0 litros', 'precio_venta': 7000.00, 'precio_compra': 3500.00},
            {'tipo': 'motor_electrico', 'nombre': 'Motor Eléctrico 400kW', 'descripcion': 'Motor eléctrico de 400kW', 'precio_venta': 8000.00, 'precio_compra': 4000.00},
            
            # Tapicerías
            {'tipo': 'tapiceria_cuero_negro', 'nombre': 'Tapicería Cuero Negro', 'descripcion': 'Tapicería de cuero negro premium', 'precio_venta': 2000.00, 'precio_compra': 1000.00},
            {'tipo': 'tapiceria_alcantara', 'nombre': 'Tapicería Alcantara Roja', 'descripcion': 'Tapicería de alcantara roja deportiva', 'precio_venta': 2500.00, 'precio_compra': 1250.00},
            {'tipo': 'tapiceria_tela', 'nombre': 'Tapicería Tela Gris', 'descripcion': 'Tapicería de tela gris deportiva', 'precio_venta': 1500.00, 'precio_compra': 750.00},
            
            # Extras
            {'tipo': 'extra_techo', 'nombre': 'Techo Panorámico', 'descripcion': 'Techo panorámico con control eléctrico', 'precio_venta': 3000.00, 'precio_compra': 1500.00},
            {'tipo': 'extra_sonido', 'nombre': 'Sistema de Sonido Premium', 'descripcion': 'Sistema de sonido premium con 12 altavoces', 'precio_venta': 2000.00, 'precio_compra': 1000.00},
            {'tipo': 'extra_asistente', 'nombre': 'Asistente de Conducción', 'descripcion': 'Sistema de asistencia a la conducción', 'precio_venta': 4000.00, 'precio_compra': 2000.00},
        ]

        # Crear componentes y stock
        for data in componentes_data:
            componente, created = Componente.objects.get_or_create(
                tipo=data['tipo'],
                defaults={
                    'nombre': data['nombre'],
                    'descripcion': data['descripcion'],
                    'precio_venta': Decimal(str(data['precio_venta'])),
                    'precio_compra': Decimal(str(data['precio_compra']))
                }
            )
            
            if created:
                self.stdout.write(f'Componente creado: {componente.nombre}')
            
            # Crear stock inicial
            stock, created = Stock.objects.get_or_create(
                componente=componente,
                defaults={
                    'cantidad': 10,
                    'stock_minimo': 5,
                    'stock_maximo': 20,
                    'ubicacion': f'Almacén {componente.tipo.split("_")[0].title()}',
                    'notas': f'Stock inicial para {componente.nombre}'
                }
            )
            
            if created:
                self.stdout.write(f'Stock creado para: {componente.nombre}')
            
            # Crear movimiento de entrada inicial
            MovimientoStock.objects.create(
                componente=componente,
                tipo='entrada',
                cantidad=10,
                precio_unitario=componente.precio_compra,
                precio_total=componente.precio_compra * Decimal('10')
            )

        self.stdout.write(self.style.SUCCESS('Datos de stock generados exitosamente')) 