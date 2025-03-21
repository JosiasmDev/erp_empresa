import os
import django
import random
from datetime import datetime, timedelta
import time
from decimal import Decimal

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

from django.contrib.auth.models import User
from ecommerce.models import Coche, Pedido as PedidoEcommerce
from human_resources.models import Empleado, Sueldo
from manufacturing.models import OrdenFabricacion, ComponenteOrden
from accounting.models import Cuenta, Balance, Factura
from inventory.models import Componente
from sales.models import Pedido as PedidoVentas
from crm.models import Cliente
from django.utils import timezone

def generar_compra_aleatoria():
    try:
        # Obtener un cliente aleatorio
        clientes = User.objects.filter(groups__name='Clientes')
        if not clientes.exists():
            print("No hay clientes registrados")
            return
        
        usuario_cliente = random.choice(clientes)
        
        # Obtener o crear el cliente en el módulo CRM
        cliente, creado = Cliente.objects.get_or_create(
            usuario=usuario_cliente,
            defaults={
                'nombre': usuario_cliente.username,
                'email': usuario_cliente.email,
                'telefono': '000000000',
                'direccion': 'Dirección por defecto'
            }
        )
        
        # Obtener un coche aleatorio con precio base
        coches = Coche.objects.filter(precio_base__isnull=False)
        if not coches.exists():
            print("No hay coches disponibles con precio base definido")
            return
        
        coche = random.choice(coches)
        
        # Crear el pedido de ecommerce
        pedido_ecommerce = PedidoEcommerce.objects.create(
            cliente=usuario_cliente,
            coche=coche,
            fecha_pedido=timezone.now(),
            estado='pendiente',
            precio_total=coche.precio_base,
            rueda_seleccionada=coche.rueda,
            motorizacion_seleccionada=coche.motorizacion,
            tapiceria_seleccionada=coche.tapiceria,
            extras_seleccionados=coche.extras
        )
        
        # Crear el pedido en el módulo de ventas
        pedido_ventas = PedidoVentas.objects.create(
            cliente=cliente,
            coche=coche,
            fecha=timezone.now(),
            estado='pendiente',
            total=coche.precio_base,
            color='Negro',
            rueda='19"'
        )
        
        # Obtener o crear componentes necesarios
        ruedas = Componente.objects.get_or_create(
            nombre='Ruedas',
            defaults={
                'descripcion': 'Ruedas del vehículo',
                'tipo': 'ruedas_19',
                'precio_venta': Decimal('1000.00')
            }
        )[0]
        
        motor = Componente.objects.get_or_create(
            nombre='Motor',
            defaults={
                'descripcion': 'Motor del vehículo',
                'tipo': 'motor_v6',
                'precio_venta': Decimal('5000.00')
            }
        )[0]
        
        tapiceria = Componente.objects.get_or_create(
            nombre='Tapicería',
            defaults={
                'descripcion': 'Tapicería del vehículo',
                'tipo': 'tapiceria_cuero_negro',
                'precio_venta': Decimal('2000.00')
            }
        )[0]
        
        extras = Componente.objects.get_or_create(
            nombre='Extras',
            defaults={
                'descripcion': 'Extras del vehículo',
                'tipo': 'extra_techo',
                'precio_venta': Decimal('3000.00')
            }
        )[0]
        
        # Crear orden de producción
        orden_produccion = OrdenFabricacion.objects.create(
            fecha_inicio=timezone.now(),
            estado='pendiente',
            coche=coche,
            pedido=pedido_ventas,
            ruedas_disponibles=True,
            motorizacion_disponible=True,
            tapiceria_disponible=True,
            extras_disponibles=True,
            ruedas_asignadas=ruedas,
            motorizacion_asignada=motor,
            tapiceria_asignada=tapiceria,
            extras_asignados=extras
        )
        
        # Crear componentes de la orden
        ComponenteOrden.objects.create(
            orden=orden_produccion,
            componente=ruedas,
            cantidad=4,
            es_extra=False
        )
        ComponenteOrden.objects.create(
            orden=orden_produccion,
            componente=motor,
            cantidad=1,
            es_extra=False
        )
        ComponenteOrden.objects.create(
            orden=orden_produccion,
            componente=tapiceria,
            cantidad=1,
            es_extra=False
        )
        ComponenteOrden.objects.create(
            orden=orden_produccion,
            componente=extras,
            cantidad=1,
            es_extra=True
        )
        
        # Crear cuenta de venta
        cuenta_venta = Cuenta.objects.create(
            tipo='venta',
            descripcion=f'Venta de vehículo {coche.nombre}',
            monto=pedido_ecommerce.precio_total,
            pedido=pedido_ecommerce
        )
        
        # Crear factura
        subtotal = pedido_ecommerce.precio_total
        iva = subtotal * Decimal('0.21')  # 21% IVA
        total = subtotal + iva
        
        factura = Factura.objects.create(
            tipo='venta',
            estado='pendiente',
            descripcion=f'Factura de venta de vehículo {coche.nombre}',
            subtotal=subtotal,
            iva=iva,
            total=total,
            cuenta=cuenta_venta
        )
        
        print(f"Pedido generado: {pedido_ecommerce.id} - Cliente: {usuario_cliente.username} - Coche: {coche.nombre}")
        print(f"Orden de producción creada: {orden_produccion.id}")
        print(f"Factura creada: {factura.id}")
        
    except Exception as e:
        print(f"Error al generar pedido: {str(e)}")
        import traceback
        print(traceback.format_exc())

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
                
                # Crear registro de gasto
                Balance.objects.create(
                    fecha=timezone.now(),
                    ingresos_totales=Decimal('0'),
                    gastos_totales=sueldo.monto,
                    salarios_totales=sueldo.monto,
                    compras_totales=Decimal('0'),
                    ventas_totales=Decimal('0'),
                    balance_total=-sueldo.monto
                )
                
                print(f"Salario pagado a: {empleado.nombre} - Monto: {empleado.sueldo_base}")
    except Exception as e:
        print(f"Error al pagar salarios: {str(e)}")
        import traceback
        print(traceback.format_exc())

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