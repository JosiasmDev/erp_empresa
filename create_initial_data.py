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
from ecommerce.models import Coche, Pedido
from crm.models import Cliente
from manufacturing.models import OrdenFabricacion, ComponenteOrden
from sales.models import Pedido as SalesPedido

User = get_user_model()
admin = User.objects.get(username='Josias')

# Crear coches si no existen
coches_data = [
    {
        'nombre': 'Eclipse',
        'precio_base': Decimal('50000.00'),
        'potencia': 300,
        'velocidad_maxima': 250,
        'descripcion': 'Un coche deportivo de alto rendimiento con diseño aerodinámico y tecnología de vanguardia.',
        'color': 'Negro',
        'rueda': '19"',
        'motorizacion': 'V6 3.0L',
        'tapiceria': 'Cuero Negro',
        'extras': 'Ninguno'
    },
    {
        'nombre': 'Arrow',
        'precio_base': Decimal('45000.00'),
        'potencia': 250,
        'velocidad_maxima': 230,
        'descripcion': 'Un coche elegante y eficiente, perfecto para el uso diario y viajes largos.',
        'color': 'Azul',
        'rueda': '17"',
        'motorizacion': 'V6 3.0L',
        'tapiceria': 'Tela Gris',
        'extras': 'Ninguno'
    }
]

for coche_data in coches_data:
    coche, created = Coche.objects.get_or_create(
        nombre=coche_data['nombre'],
        defaults=coche_data
    )
    if created:
        print(f"Coche creado: {coche.nombre}")
    else:
        print(f"Coche ya existía: {coche.nombre}")

# Crear componentes
componentes_data = [
    {
        'nombre': 'Ruedas 17"',
        'tipo': 'ruedas_17',
        'descripcion': 'Ruedas deportivas de 17 pulgadas',
        'precio_venta': Decimal('150.00')
    },
    {
        'nombre': 'Ruedas 19"',
        'tipo': 'ruedas_19',
        'descripcion': 'Ruedas deportivas de 19 pulgadas',
        'precio_venta': Decimal('200.00')
    },
    {
        'nombre': 'Ruedas 21"',
        'tipo': 'ruedas_21',
        'descripcion': 'Ruedas deportivas de 21 pulgadas',
        'precio_venta': Decimal('300.00')
    },
    {
        'nombre': 'Motor V6',
        'tipo': 'motor_v6',
        'descripcion': 'Motor V6 3.0L de alto rendimiento',
        'precio_venta': Decimal('5000.00')
    },
    {
        'nombre': 'Motor V8',
        'tipo': 'motor_v8',
        'descripcion': 'Motor V8 4.0L de alto rendimiento',
        'precio_venta': Decimal('7000.00')
    },
    {
        'nombre': 'Motor Eléctrico',
        'tipo': 'motor_electrico',
        'descripcion': 'Motor Eléctrico 400kW de alto rendimiento',
        'precio_venta': Decimal('8000.00')
    },
    {
        'nombre': 'Tapicería Cuero Negro',
        'tipo': 'tapiceria_cuero_negro',
        'descripcion': 'Tapicería de cuero negro premium',
        'precio_venta': Decimal('1000.00')
    },
    {
        'nombre': 'Tapicería Alcantara',
        'tipo': 'tapiceria_alcantara',
        'descripcion': 'Tapicería de alcantara roja deportiva',
        'precio_venta': Decimal('1500.00')
    },
    {
        'nombre': 'Tapicería Tela',
        'tipo': 'tapiceria_tela',
        'descripcion': 'Tapicería de tela gris deportiva',
        'precio_venta': Decimal('500.00')
    },
    {
        'nombre': 'Techo Panorámico',
        'tipo': 'extra_techo',
        'descripcion': 'Techo panorámico con control electrónico',
        'precio_venta': Decimal('2000.00')
    },
    {
        'nombre': 'Sistema de Sonido',
        'tipo': 'extra_sonido',
        'descripcion': 'Sistema de sonido premium con 12 altavoces',
        'precio_venta': Decimal('800.00')
    },
    {
        'nombre': 'Asistente de Conducción',
        'tipo': 'extra_asistente',
        'descripcion': 'Sistema avanzado de asistencia a la conducción',
        'precio_venta': Decimal('1500.00')
    }
]

# Guardar componentes
for componente_data in componentes_data:
    componente, created = Componente.objects.get_or_create(
        tipo=componente_data['tipo'],
        defaults=componente_data
    )
    if created:
        print(f"Componente creado: {componente.nombre}")
    else:
        print(f"Componente ya existía: {componente.nombre}")

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
    
    # Crear empleado solo si no existe
    empleado, created = Empleado.objects.get_or_create(
        usuario=user,
        defaults={
            'nombre': modulo.capitalize(),
            'cargo': modulo,
            'sueldo_base': salarios_base[modulo],
            'activo': True
        }
    )
    if created:
        print(f"Empleado creado: {username}")
        
        # Crear sueldo inicial solo para empleados nuevos
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

# Crear usuario para el cliente demo
cliente_user, created = User.objects.get_or_create(
    username='cliente_demo',
    defaults={
        'email': 'cliente@demo.com',
        'first_name': 'Cliente',
        'last_name': 'Demo'
    }
)
if created:
    cliente_user.set_password('aaaaaa')
    cliente_user.save()
    print("Usuario cliente demo creado")

# Crear 4 pedidos aleatorios para Josias
coches = Coche.objects.all()
for i in range(4):
    coche = random.choice(coches)
    
    # Seleccionar componentes aleatorios
    color = random.choice(['Negro', 'Rojo', 'Azul', 'Blanco'])
    rueda = random.choice(['17"', '19"', '21"'])
    motorizacion = random.choice(['V6 3.0L', 'V8 4.0L', 'Eléctrico 400kW'])
    tapiceria = random.choice(['Cuero Negro', 'Alcantara Roja', 'Tela Gris'])
    extras = random.choice(['Ninguno', 'Techo Panorámico', 'Sistema de Sonido Premium', 'Asistente de Conducción'])
    
    # Actualizar el coche con el color seleccionado
    coche.color = color
    coche.save()
    
    # Generar número de pedido único más corto
    timestamp = datetime.now().strftime('%H%M%S')  # Solo horas, minutos y segundos
    numero_pedido = f"PED-{timestamp}-{i+1}"  # Formato: PED-HHMMSS-N
    
    # Crear pedido de ecommerce
    pedido_ecommerce = Pedido.objects.create(
        numero_pedido=numero_pedido,
        cliente=cliente_user,
        coche=coche,
        estado='pendiente',
        precio_total=coche.precio_base
    )
    
    # Crear pedido de ventas
    pedido_ventas = SalesPedido.objects.create(
        cliente=cliente,
        coche=coche,
        color=random.choice(['Negro', 'Rojo', 'Azul', 'Blanco']),
        rueda=random.choice(['17"', '19"', '21"']),
        estado='pendiente'
    )
    pedido_ventas.calcular_total()
    
    print(f"Pedido {i+1} creado para Josias con coche {coche.nombre}")
    print(f"  - Color: {color}")
    print(f"  - Ruedas: {rueda}")
    print(f"  - Motorización: {motorizacion}")
    print(f"  - Tapicería: {tapiceria}")
    print(f"  - Extras: {extras}")
    
    # Crear orden de producción
    timestamp = datetime.now().strftime('%H%M%S%f')  # Incluir microsegundos
    numero_orden = f"OF-{timestamp}-{i+1}"  # Formato: OF-HHMMSSMMM-N
    orden = OrdenFabricacion.objects.create(
        pedido=pedido_ventas,  # Usar el pedido de ventas
        coche=coche,
        estado='pendiente',
        numero_orden=numero_orden  # Asignar número de orden único
    ) 
    
    # Asignar componentes a la orden
    if rueda == '17"':
        orden.ruedas_asignadas = Componente.objects.filter(tipo='ruedas_17').first()
    elif rueda == '19"':
        orden.ruedas_asignadas = Componente.objects.filter(tipo='ruedas_19').first()
    else:  # 21"
        orden.ruedas_asignadas = Componente.objects.filter(tipo='ruedas_21').first()
    
    if motorizacion == 'V6 3.0L':
        orden.motorizacion_asignada = Componente.objects.filter(tipo='motor_v6').first()
    elif motorizacion == 'V8 4.0L':
        orden.motorizacion_asignada = Componente.objects.filter(tipo='motor_v8').first()
    else:  # Eléctrico
        orden.motorizacion_asignada = Componente.objects.filter(tipo='motor_electrico').first()
    
    if tapiceria == 'Cuero Negro':
        orden.tapiceria_asignada = Componente.objects.filter(tipo='tapiceria_cuero_negro').first()
    elif tapiceria == 'Alcantara Roja':
        orden.tapiceria_asignada = Componente.objects.filter(tipo='tapiceria_alcantara').first()
    else:  # Tela Gris
        orden.tapiceria_asignada = Componente.objects.filter(tipo='tapiceria_tela').first()
    
    if extras != 'Ninguno':
        if extras == 'Techo Panorámico':
            orden.extras_asignados = Componente.objects.filter(tipo='extra_techo').first()
        elif extras == 'Sistema de Sonido Premium':
            orden.extras_asignados = Componente.objects.filter(tipo='extra_sonido').first()
        else:  # Asistente de Conducción
            orden.extras_asignados = Componente.objects.filter(tipo='extra_asistente').first()
    
    orden.save()
    print(f"  - Orden de producción creada: {orden.numero_orden}")
    
    # Crear componentes de la orden
    ComponenteOrden.objects.create(orden=orden, componente=orden.ruedas_asignadas, cantidad=4)
    ComponenteOrden.objects.create(orden=orden, componente=orden.motorizacion_asignada, cantidad=1)
    ComponenteOrden.objects.create(orden=orden, componente=orden.tapiceria_asignada, cantidad=1)
    if orden.extras_asignados:
        ComponenteOrden.objects.create(orden=orden, componente=orden.extras_asignados, cantidad=1, es_extra=True)

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