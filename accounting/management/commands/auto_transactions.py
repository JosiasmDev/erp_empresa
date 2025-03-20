from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
import random
import time
from inventory.models import Componente
from accounting.models import Cuenta
from human_resources.models import Empleado
from sales.models import Pedido

class Command(BaseCommand):
    help = 'Genera transacciones automáticas: compras de vehículos y pago de sueldos'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando generación automática de transacciones...')
        
        while True:
            try:
                # Cada 30 segundos: Generar 2 compras aleatorias
                self.generar_compras_aleatorias()
                time.sleep(30)
                
                # Cada minuto: Pagar sueldos
                self.pagar_sueldos()
                time.sleep(30)  # Esperar otros 30 segundos para completar el minuto
                
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS('Deteniendo generación de transacciones'))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
                time.sleep(5)  # Esperar un poco antes de reintentar
    
    def generar_compras_aleatorias(self):
        # Obtener usuarios y componentes disponibles
        usuarios = User.objects.all()
        componentes = Componente.objects.all()
        
        if not usuarios or not componentes:
            return
        
        # Generar 2 compras aleatorias
        for _ in range(2):
            try:
                usuario = random.choice(usuarios)
                componentes_seleccionados = random.sample(list(componentes), k=random.randint(1, 3))
                
                # Calcular total de la compra
                total = sum(comp.precio_venta for comp in componentes_seleccionados)
                
                # Crear pedido
                pedido = Pedido.objects.create(
                    usuario=usuario,
                    fecha=timezone.now(),
                    estado='completado',
                    total=total
                )
                
                # Registrar la compra en contabilidad
                Cuenta.objects.create(
                    tipo='venta',
                    monto=total,
                    descripcion=f'Venta automática - Pedido #{pedido.id}',
                    fecha=timezone.now()
                )
                
                self.stdout.write(self.style.SUCCESS(
                    f'Compra generada: Usuario={usuario.username}, Total={total}€'
                ))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al generar compra: {str(e)}'))
    
    def pagar_sueldos(self):
        # Obtener todos los empleados activos
        empleados = Empleado.objects.filter(activo=True)
        
        if not empleados:
            return
        
        total_sueldos = Decimal('0')
        
        # Pagar sueldo a cada empleado
        for empleado in empleados:
            try:
                # Registrar el pago del sueldo
                Cuenta.objects.create(
                    tipo='salario',
                    monto=empleado.sueldo,
                    descripcion=f'Pago de sueldo - {empleado.nombre}',
                    fecha=timezone.now(),
                    empleado=empleado
                )
                
                total_sueldos += empleado.sueldo
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Error al pagar sueldo a {empleado.nombre}: {str(e)}'
                ))
        
        self.stdout.write(self.style.SUCCESS(
            f'Sueldos pagados: {len(empleados)} empleados, Total={total_sueldos}€'
        )) 