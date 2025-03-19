from django.utils import timezone
from django.contrib.auth.models import User
from ecommerce.models import Coche, Pedido
from human_resources.models import Empleado, Sueldo
from accounting.models import Cuenta
from decimal import Decimal
import random
from django.db.models import F
from manufacturing.models import OrdenFabricacion
from inventory.models import OrdenEntrega

def procesar_sueldos():
    """Procesa los sueldos de todos los empleados activos cada minuto"""
    empleados = Empleado.objects.filter(activo=True)
    
    for empleado in empleados:
        # Crear registro de sueldo
        sueldo = Sueldo.objects.create(
            empleado=empleado,
            monto=empleado.sueldo_base
        )
        
        # Registrar el gasto en contabilidad
        Cuenta.objects.create(
            tipo='salario',
            descripcion=f'Sueldo de {empleado.usuario.username}',
            monto=empleado.sueldo_base,
            empleado=empleado.usuario
        )

def generar_compras_aleatorias():
    """Genera 3 compras aleatorias cada minuto"""
    coches = list(Coche.objects.all())
    if not coches:
        return
    
    for _ in range(3):
        coche = random.choice(coches)
        # Crear pedido
        pedido = Pedido.objects.create(
            cliente=None,  # Cliente anónimo
            coche=coche,
            precio_total=coche.precio_base,
            rueda_seleccionada=random.choice(['17"', '19"', '21"']),
            motorizacion_seleccionada=random.choice(['Básica', 'Media', 'Premium']),
            tapiceria_seleccionada=random.choice(['Tela', 'Cuero', 'Alcantara']),
            extras_seleccionados=random.choice(['Ninguno', 'GPS', 'Sistema de Sonido', 'Asientos Calefactables']),
            estado='pendiente'
        )
        
        # Crear orden de fabricación
        OrdenFabricacion.objects.create(
            pedido=pedido,
            coche=coche,
            estado='pendiente'
        )
        
        # Crear orden de entrega
        OrdenEntrega.objects.create(
            pedido=pedido,
            estado='pendiente'
        )
        
        # Registrar la venta en contabilidad
        Cuenta.objects.create(
            tipo='venta',
            descripcion=f'Venta aleatoria del coche {coche.nombre}',
            monto=coche.precio_base,
            pedido=pedido
        )

def pagar_salarios():
    """Paga los salarios mensuales a todos los empleados"""
    empleados = Empleado.objects.all()
    for empleado in empleados:
        Cuenta.objects.create(
            tipo='salario',
            descripcion=f'Pago de salario mensual a {empleado.nombre}',
            monto=empleado.salario,
            empleado=empleado.user
        )

def ejecutar_tareas_programadas():
    """Ejecuta todas las tareas programadas"""
    # Generar 3 compras aleatorias
    for _ in range(3):
        generar_compras_aleatorias()
    
    # Verificar si es fin de mes para pagar salarios
    hoy = timezone.now()
    if hoy.day == 1:  # Si es el primer día del mes
        pagar_salarios() 