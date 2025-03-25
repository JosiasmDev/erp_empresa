import os
import django
from decimal import Decimal
import random
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_empresa.settings')
django.setup()

from inventory.models import Componente, Stock, MovimientoStock
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from human_resources.models import Empleado, Sueldo
from sales.models import Pedido, PedidoItem
from ecommerce.models import Coche
from crm.models import Cliente

User = get_user_model()
admin = User.objects.get(username='Josias')

# Crear componentes
componentes = [
    Componente(
        nombre='Ruedas 17"',
        tipo='ruedas_17',
        descripcion='Ruedas deportivas de 17 pulgadas',
        precio_venta=Decimal('150.00')
    ),
    Componente(
        nombre='Ruedas 19"',
        tipo='ruedas_19',
        descripcion='Ruedas deportivas de 19 pulgadas',
        precio_venta=Decimal('200.00')
    ),
    Componente(
        nombre='Ruedas 21"',
        tipo='ruedas_21',
        descripcion='Ruedas deportivas de 21 pulgadas',
        precio_venta=Decimal('300.00')
    ),
    Componente(
        nombre='Motor V6',
        tipo='motor_v6',
        descripcion='Motor V6 3.0L de alto rendimiento',
        precio_venta=Decimal('5000.00')
    ),
    Componente(
        nombre='Motor V8',
        tipo='motor_v8',
        descripcion='Motor V8 4.0L de alto rendimiento',
        precio_venta=Decimal('7000.00')
    ),
    Componente(
        nombre='Motor Eléctrico',
        tipo='motor_electrico',
        descripcion='Motor Eléctrico 400kW de alto rendimiento',
        precio_venta=Decimal('8000.00')
    ),
    Componente(
        nombre='Tapicería Cuero Negro',
        tipo='tapiceria_cuero_negro',
        descripcion='Tapicería de cuero negro premium',
        precio_venta=Decimal('1000.00')
    ),
    Componente(
        nombre='Tapicería Alcantara',
        tipo='tapiceria_alcantara',
        descripcion='Tapicería de alcantara roja deportiva',
        precio_venta=Decimal('1500.00')
    ),
    Componente(
        nombre='Tapicería Tela',
        tipo='tapiceria_tela',
        descripcion='Tapicería de tela gris deportiva',
        precio_venta=Decimal('500.00')
    ),
    Componente(
        nombre='Techo Panorámico',
        tipo='extra_techo',
        descripcion='Techo panorámico con control electrónico',
        precio_venta=Decimal('2000.00')
    ),
    Componente(
        nombre='Sistema de Sonido',
        tipo='extra_sonido',
        descripcion='Sistema de sonido premium con 12 altavoces',
        precio_venta=Decimal('800.00')
    ),
    Componente(
        nombre='Asistente de Conducción',
        tipo='extra_asistente',
        descripcion='Sistema avanzado de asistencia a la conducción',
        precio_venta=Decimal('1500.00')
    )
]

# Guardar componentes
for componente in componentes:
    componente.save()
    print(f"Componente creado: {componente.nombre}")

# Crear stock para cada componente
for componente in Componente.objects.all():
    stock, created = Stock.objects.get_or_create(
        componente=componente,
        defaults={
            'cantidad': 20,
            'stock_minimo': 5,
            'stock_maximo': 200,
            'ubicacion': 'Almacén Principal',
            'notas': 'Stock inicial'
        }
    )
    if created:
        print(f"Stock creado para: {componente.nombre}")
    else:
        print(f"Stock ya existía para: {componente.nombre}")

# Crear movimientos de stock iniciales
for componente in Componente.objects.all():
    MovimientoStock.objects.create(
        componente=componente,
        tipo='entrada',
        cantidad=20,
        precio_unitario=componente.precio_compra,
        usuario=admin
    )
    print(f"Movimiento de stock creado para: {componente.nombre}")

# Crear grupos por módulo y sus usuarios
modulos = [
    'inventory',
    'sales', 
    'accounting',
    'human_resources',
    'manufacturing',
    'crm',
    'ecommerce'
]

salarios_base = {
    'inventory': Decimal('25.00'),
    'sales': Decimal('30.00'),
    'accounting': Decimal('28.00'),
    'human_resources': Decimal('27.00'),
    'manufacturing': Decimal('26.00'),
    'crm': Decimal('24.00'),
    'ecommerce': Decimal('29.00')
}

for modulo in modulos:
    # Crear grupo si no existe
    grupo, created = Group.objects.get_or_create(name=modulo)
    if created:
        print(f"Grupo creado: {modulo}")
    
    # Crear usuario
    username = modulo
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@empresa.com',
            'first_name': modulo.capitalize(),
            'last_name': 'Usuario'
        }
    )
    if created:
        user.set_password('aaaaaa')
        user.save()
        user.groups.add(grupo)
        print(f"Usuario creado: {username}")
    
    # Crear empleado
    empleado = Empleado.objects.create(
        usuario=user,
        nombre=modulo.capitalize(),
        cargo=modulo,
        sueldo_base=salarios_base[modulo],
        activo=True
    )
    print(f"Empleado creado: {username}")
    
    # Crear sueldo inicial
    Sueldo.objects.create(
        empleado=empleado,
        monto=salarios_base[modulo],
        pagado=True
    )
    print(f"Sueldo creado para: {username}")

# Crear cliente para los pedidos
cliente, created = Cliente.objects.get_or_create(
    nombre='Cliente Demo',
    defaults={
        'email': 'cliente@demo.com',
        'telefono': '123456789'
    }
)

# Crear 4 pedidos aleatorios para Josias
coches = Coche.objects.all()
for i in range(4):
    coche = random.choice(coches)
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
    
    print(f"Pedido {i+1} creado para Josias con coche {coche.nombre}")

# Verificar
print("\nResumen:")
print(f"Total de componentes: {Componente.objects.count()}")
print(f"Total de stock: {Stock.objects.count()}")
print(f"Total de movimientos: {MovimientoStock.objects.count()}")
print(f"Total de empleados: {Empleado.objects.count()}")
print(f"Total de pedidos: {Pedido.objects.count()}")

# Iniciar auto_transactions.py en segundo plano
import subprocess
subprocess.Popen(['python', 'auto_transactions.py'], 
                 creationflags=subprocess.CREATE_NEW_CONSOLE)
print("\nAuto transactions iniciado en segundo plano") 