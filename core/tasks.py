from django.utils import timezone
from django.contrib.auth.models import User
from ecommerce.models import Coche, Pedido
from human_resources.models import Empleado
from accounting.models import Cuenta
from decimal import Decimal
import random

def generar_compra_aleatoria():
    """Genera una compra aleatoria de un coche"""
    coches = list(Coche.objects.all())
    if not coches:
        return
    
    coche = random.choice(coches)
    clientes = list(User.objects.filter(groups__name='cliente'))
    if not clientes:
        return
    
    cliente = random.choice(clientes)
    
    # Crear pedido
    pedido = Pedido.objects.create(
        cliente=cliente,
        coche=coche,
        precio_total=coche.precio_base,
        rueda_seleccionada=coche.rueda,
        motorizacion_seleccionada=coche.motorizacion,
        tapiceria_seleccionada=coche.tapiceria,
        extras_seleccionados=coche.extras
    )
    
    # Registrar en contabilidad
    Cuenta.objects.create(
        tipo='venta',
        descripcion=f'Venta aleatoria del coche {coche.nombre} - Pedido {pedido.numero_pedido}',
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
        generar_compra_aleatoria()
    
    # Verificar si es fin de mes para pagar salarios
    hoy = timezone.now()
    if hoy.day == 1:  # Si es el primer día del mes
        pagar_salarios() 