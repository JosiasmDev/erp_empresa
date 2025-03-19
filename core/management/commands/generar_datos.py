from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from core.models import Employee, ProductionOrder, PurchaseOrder, Inventory
from decimal import Decimal
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Genera datos de ejemplo para el sistema ERP'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generando datos de ejemplo...')

        # Crear grupos de usuarios
        grupos = [
            'ventas', 'compras', 'produccion', 'inventario', 
            'rrhh', 'marketing', 'contabilidad', 'website'
        ]
        grupos_creados = []
        for grupo in grupos:
            grupo_obj, _ = Group.objects.get_or_create(name=grupo)
            grupos_creados.append(grupo_obj)
            self.stdout.write(f'Grupo creado/existente: {grupo}')

        # Crear superusuario si no existe
        admin_user = User.objects.filter(username='admin').first()
        if not admin_user:
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Superusuario creado: admin/admin')
        
        # Asignar todos los grupos al admin
        for grupo in grupos_creados:
            admin_user.groups.add(grupo)
        admin_user.save()
        self.stdout.write('Grupos asignados al superusuario admin')

        # Crear empleados
        puestos = ['Vendedor', 'Comprador', 'Operario', 'Almacenista', 'RRHH', 'Marketing']
        for i in range(10):
            empleado = Employee.objects.create(
                nombre=f'Empleado {i+1}',
                puesto=random.choice(puestos),
                salario_base=Decimal(str(random.randint(1500, 3000))),
                fecha_contratacion=datetime.now() - timedelta(days=random.randint(1, 365)),
                activo=True
            )
            self.stdout.write(f'Empleado creado: {empleado.nombre}')

        # Crear materiales en inventario
        materiales = [
            'Motor', 'Transmisión', 'Chasis', 'Ruedas', 'Asientos',
            'Volante', 'Batería', 'Pintura', 'Vidrios', 'Sistema Eléctrico'
        ]
        for material in materiales:
            inv = Inventory.objects.create(
                material=material,
                cantidad=random.randint(10, 100),
                precio_unitario=Decimal(str(random.randint(100, 1000)))
            )
            self.stdout.write(f'Material creado: {inv.material}')

        # Crear órdenes de compra
        estados_compra = ['pendiente', 'en_proceso', 'completada']
        for i in range(5):
            orden = PurchaseOrder.objects.create(
                material=random.choice(materiales),
                cantidad=random.randint(5, 20),
                precio_total=Decimal(str(random.randint(1000, 5000))),
                fecha_pedido=datetime.now() - timedelta(days=random.randint(1, 30)),
                estado=random.choice(estados_compra)
            )
            self.stdout.write(f'Orden de compra creada: {orden.id}')

        # Crear órdenes de producción
        estados_produccion = ['pendiente', 'en_proceso', 'completada']
        for i in range(5):
            orden = ProductionOrder.objects.create(
                producto='Vehículo Modelo ' + str(random.randint(1, 5)),
                cantidad=random.randint(1, 5),
                fecha_inicio=datetime.now() - timedelta(days=random.randint(1, 30)),
                estado=random.choice(estados_produccion),
                materiales_disponibles=random.choice([True, False]),
                completada=False
            )
            self.stdout.write(f'Orden de producción creada: {orden.id}')

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo generados exitosamente')) 