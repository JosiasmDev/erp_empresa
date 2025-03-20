import os
import django
import random
from datetime import datetime, timedelta
import time

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

from django.contrib.auth.models import User
from ecommerce.models import Coche, Pedido as PedidoEcommerce
from human_resources.models import Empleado, Sueldo
from manufacturing.models import OrdenFabricacion, ComponenteOrden
from accounting.models import Cuenta, Balance, Factura
from django.utils import timezone

def generar_compra_aleatoria():
    try:
        # Obtener un cliente aleatorio
        clientes = User.objects.filter(groups__name='Clientes')
        if not clientes.exists():
            print("No hay clientes registrados")
            return
        
        cliente = random.choice(clientes)
        
        # Obtener un coche aleatorio
        coches = Coche.objects.all()
        if not coches.exists():
            print("No hay coches disponibles")
            return
        
        coche = random.choice(coches)
        
        # Crear el pedido de ecommerce
        pedido_ecommerce = PedidoEcommerce.objects.create(
            cliente=cliente,
            coche=coche,
            fecha_pedido=timezone.now(),
            estado='pendiente',
            precio_total=coche.precio_base,
            rueda_seleccionada=coche.rueda,
            motorizacion_seleccionada=coche.motorizacion,
            tapiceria_seleccionada=coche.tapiceria,
            extras_seleccionados=coche.extras
        )
        
        # Crear orden de producción
        orden_produccion = OrdenFabricacion.objects.create(
            fecha_inicio=timezone.now(),
            estado='pendiente',
            coche=coche
        )
        
        # Crear componentes de la orden
        ComponenteOrden.objects.create(
            orden=orden_produccion,
            componente_id=1,  # Asumiendo que 1 es el ID del componente Chasis
            cantidad=1,
            es_extra=False
        )
        ComponenteOrden.objects.create(
            orden=orden_produccion,
            componente_id=2,  # Asumiendo que 2 es el ID del componente Motor
            cantidad=1,
            es_extra=False
        )
        ComponenteOrden.objects.create(
            orden=orden_produccion,
            componente_id=3,  # Asumiendo que 3 es el ID del componente Carrocería
            cantidad=1,
            es_extra=False
        )
        
        # Crear cuenta de venta
        cuenta_venta = Cuenta.objects.create(
            tipo='venta',
            descripcion=f'Venta de vehículo {coche.nombre}',
            monto=pedido_ecommerce.precio_total,
            pedido=pedido_ecommerce
        )
        
        # Crear factura
        factura = Factura.objects.create(
            tipo='venta',
            estado='pendiente',
            descripcion=f'Factura de venta de vehículo {coche.nombre}',
            subtotal=pedido_ecommerce.precio_total,
            total=pedido_ecommerce.precio_total * 1.21,  # Incluyendo IVA
            cuenta=cuenta_venta
        )
        
        print(f"Pedido generado: {pedido_ecommerce.id} - Cliente: {cliente.username} - Coche: {coche.nombre}")
        print(f"Orden de producción creada: {orden_produccion.id}")
        print(f"Factura creada: {factura.id}")
        
    except Exception as e:
        print(f"Error al generar pedido: {str(e)}")

def pagar_salarios():
    try:
        # Obtener todos los empleados
        empleados = Empleado.objects.all()
        
        for empleado in empleados:
            # Verificar si ya se pagó el salario en el último minuto
            ultimo_pago = Sueldo.objects.filter(
                empleado=empleado,
                fecha__gte=timezone.now() - timedelta(minutes=1)
            ).first()
            
            if not ultimo_pago:
                # Crear nuevo pago de salario
                sueldo = Sueldo.objects.create(
                    empleado=empleado,
                    monto=empleado.sueldo_base,
                    fecha=timezone.now(),
                    pagado=True
                )
                
                # Registrar transacción en contabilidad
                cuenta_salario = Cuenta.objects.create(
                    tipo='salario',
                    descripcion=f'Pago de salario a {empleado.nombre}',
                    monto=sueldo.monto,
                    empleado=empleado.usuario
                )
                
                print(f"Salario pagado a: {empleado.nombre} - Monto: {empleado.sueldo_base}")
    except Exception as e:
        print(f"Error al pagar salarios: {str(e)}")

def main():
    print("Iniciando tareas automáticas...")
    print("Presione Ctrl+C para detener")
    
    while True:
        try:
            # Generar compra aleatoria cada 30 segundos
            generar_compra_aleatoria()
            time.sleep(30)
            
            # Pagar salarios cada minuto
            pagar_salarios()
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\nDeteniendo tareas automáticas...")
            break
        except Exception as e:
            print(f"Error en el bucle principal: {str(e)}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar

if __name__ == "__main__":
    main() 