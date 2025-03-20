from django.core.management.base import BaseCommand
from inventory.models import Componente
from decimal import Decimal

class Command(BaseCommand):
    help = 'Actualiza los precios de compra al 30% del precio de venta'

    def handle(self, *args, **kwargs):
        componentes = Componente.objects.all()
        for componente in componentes:
            precio_venta = componente.precio_venta
            componente.precio_compra = precio_venta * Decimal('0.3')
            componente.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Actualizado {componente.nombre}: Precio venta={precio_venta}€, '
                    f'Precio compra={componente.precio_compra}€'
                )
            ) 