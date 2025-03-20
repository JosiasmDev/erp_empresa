from django.core.management.base import BaseCommand
from django.db import transaction
from ecommerce.models import Pedido as EcommercePedido
from sales.models import Pedido as SalesPedido
from manufacturing.models import OrdenFabricacion, ComponenteOrden
from inventory.models import OrdenEntrega
from accounting.models import Factura, Cuenta

class Command(BaseCommand):
    help = 'Limpia todos los pedidos, ventas y órdenes de fabricación de la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando limpieza de datos...')
        
        try:
            with transaction.atomic():
                # Eliminar facturas relacionadas
                facturas = Factura.objects.filter(tipo='venta')
                self.stdout.write(f'Eliminando {facturas.count()} facturas...')
                facturas.delete()
                
                # Eliminar cuentas relacionadas
                cuentas = Cuenta.objects.filter(tipo__in=['venta', 'ingreso'])
                self.stdout.write(f'Eliminando {cuentas.count()} cuentas...')
                cuentas.delete()
                
                # Eliminar componentes de órdenes
                componentes = ComponenteOrden.objects.all()
                self.stdout.write(f'Eliminando {componentes.count()} componentes de órdenes...')
                componentes.delete()
                
                # Eliminar órdenes de entrega
                ordenes_entrega = OrdenEntrega.objects.all()
                self.stdout.write(f'Eliminando {ordenes_entrega.count()} órdenes de entrega...')
                ordenes_entrega.delete()
                
                # Eliminar órdenes de fabricación
                ordenes = OrdenFabricacion.objects.all()
                self.stdout.write(f'Eliminando {ordenes.count()} órdenes de fabricación...')
                ordenes.delete()
                
                # Eliminar pedidos de ventas
                pedidos_sales = SalesPedido.objects.all()
                self.stdout.write(f'Eliminando {pedidos_sales.count()} pedidos de ventas...')
                pedidos_sales.delete()
                
                # Eliminar pedidos de ecommerce
                pedidos_ecommerce = EcommercePedido.objects.all()
                self.stdout.write(f'Eliminando {pedidos_ecommerce.count()} pedidos de ecommerce...')
                pedidos_ecommerce.delete()
                
                self.stdout.write(self.style.SUCCESS('Limpieza de datos completada exitosamente'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la limpieza: {str(e)}'))
            raise 