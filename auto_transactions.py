import os
import django
import time
import random
from datetime import datetime
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

from django.contrib.auth import get_user_model
from ecommerce.models import Coche
from crm.models import Cliente
from sales.models import Pedido, PedidoItem
from human_resources.models import Empleado, Sueldo
from accounting.models import Cuenta

User = get_user_model()

def generar_compra():
    """Genera una compra aleatoria de vehículos"""
    try:
        # Obtener cliente aleatorio o crear uno nuevo
        if not Cliente.objects.exists():
            cliente = Cliente.objects.create(
                nombre='Cliente Aleatorio',
                email='cliente@random.com',
                telefono='123456789'
            )
        else:
            cliente = random.choice(Cliente.objects.all())
        
        # Obtener coche aleatorio
        coches = Coche.objects.all()
        if not coches.exists():
            print("No hay coches disponibles para vender")
            return
            
        coche = random.choice(coches)
        
        # Crear pedido
        pedido = Pedido.objects.create(
            cliente=cliente,
            coche=coche,
            color=random.choice(['Negro', 'Rojo', 'Azul', 'Blanco']),
            rueda=random.choice(['17"', '19"', '21"']),
            estado='completado'
        )
        pedido.calcular_total()
        
        # Añadir item al pedido
        PedidoItem.objects.create(
            pedido=pedido,
            coche=coche,
            cantidad=1
        )
        
        # Registrar en contabilidad
        Cuenta.objects.create(
            tipo='venta',
            monto=pedido.total,
            descripcion=f'Venta de vehículo - Pedido #{pedido.id}',
            fecha=datetime.now()
        )
        
        print(f"Compra generada: Pedido #{pedido.id} por {cliente.nombre}")
        
    except Exception as e:
        print(f"Error al generar compra: {str(e)}")

def pagar_sueldos():
    """Paga los sueldos a todos los empleados"""
    try:
        empleados = Empleado.objects.filter(activo=True)
        for empleado in empleados:
            # Crear sueldo
            Sueldo.objects.create(
                empleado=empleado,
                monto=empleado.sueldo_base,
                pagado=True
            )
            
            # Registrar en contabilidad
            Cuenta.objects.create(
                tipo='salario',
                monto=empleado.sueldo_base,
                descripcion=f'Pago de sueldo a {empleado.nombre}',
                fecha=datetime.now()
            )
            
        print(f"Sueldos pagados a {len(empleados)} empleados")
        
    except Exception as e:
        print(f"Error al pagar sueldos: {str(e)}")

def main():
    print("Iniciando generación automática de transacciones...")
    ultimo_pago_sueldos = None
    
    while True:
        try:
            # Obtener la fecha y hora actual
            ahora = datetime.now()
            
            # Verificar si es momento de pagar sueldos (cada minuto)
            if ultimo_pago_sueldos is None or (ahora - ultimo_pago_sueldos).total_seconds() >= 60:
                pagar_sueldos()
                ultimo_pago_sueldos = ahora
                print(f"Pagos de salarios ejecutados en: {ahora}")
            
            # Generar compra cada 30 segundos
            generar_compra()
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\nDeteniendo generación de transacciones...")
            break
        except Exception as e:
            print(f"Error general: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    main() 